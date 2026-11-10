"""Text Rewriting and Grammar Assistant - local classroom project."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json, os, re
from html import escape

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))
API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.environ.get("OPENAI_API_KEY", "")

PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Text Rewriting and Grammar Assistant</title>
<style>
:root{--ink:#182638;--muted:#607087;--blue:#3659d9;--pale:#f3f6fb;--line:#dce3ef;--green:#15734c}*{box-sizing:border-box}body{margin:0;background:#f7f8fc;color:var(--ink);font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}.wrap{max-width:1100px;margin:0 auto;padding:32px 22px 60px}header{margin-bottom:24px}.eyebrow{color:var(--blue);font-size:12px;letter-spacing:.12em;font-weight:750;text-transform:uppercase}h1{font-size:clamp(28px,4vw,42px);line-height:1.1;margin:8px 0}p{margin:8px 0}.sub{color:var(--muted);max-width:760px}.card{background:white;border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 7px 24px #1d2a440b;margin:16px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.control{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:10px 0}.toggle{display:flex;gap:8px;align-items:center;color:var(--muted);font-size:14px}label{font-weight:700;font-size:14px}textarea{width:100%;min-height:160px;resize:vertical;border:1px solid var(--line);border-radius:10px;padding:13px;font:inherit;color:var(--ink)}select,button{font:inherit;border-radius:9px;padding:10px 13px;border:1px solid var(--line);background:#fff;color:var(--ink)}button{background:var(--blue);border-color:var(--blue);color:white;font-weight:700;cursor:pointer}button.secondary{background:white;color:var(--blue)}button:disabled{opacity:.55;cursor:wait}.outputs{display:grid;grid-template-columns:1fr 1fr;gap:16px}.out{background:var(--pale);padding:16px;border-radius:12px;min-height:130px;white-space:pre-wrap}.tag{display:inline-block;padding:3px 8px;border-radius:999px;background:#e9edff;color:#3349ad;font-size:12px;font-weight:700;margin-left:6px}.notice{font-size:13px;color:var(--muted);background:#f5f7fb;padding:12px;border-radius:10px}.facts{border-left:4px solid var(--green);padding:12px 15px;background:#f0faf5;border-radius:0 10px 10px 0}.interpret{border-left:4px solid #b67710;padding:12px 15px;background:#fff8e9;border-radius:0 10px 10px 0}.small{font-size:13px;color:var(--muted)}footer{font-size:13px;color:var(--muted);text-align:center;margin-top:28px}@media(max-width:720px){.grid,.outputs{grid-template-columns:1fr}.card{padding:17px}}
</style></head><body><main class="wrap"><header><div class="eyebrow">Group 3 • Gen AI Project</div><h1>Text Rewriting and Grammar Assistant</h1><p class="sub">Improve clarity, grammar and readability while keeping the original meaning. Compare two rewrite styles side by side.</p></header>
<section class="card"><label for="source">Your text</label><textarea id="source" maxlength="5000" placeholder="Paste or type a paragraph to rewrite…"></textarea><div class="control"><label for="style">Rewrite style</label><select id="style"><option value="clear">Clear and concise</option><option value="formal">Formal and polished</option></select><label class="toggle"><input id="both" type="checkbox" checked> Generate both styles</label><button id="go">Rewrite text</button><span id="status" class="small" aria-live="polite"></span></div><div class="notice">Text is processed on this computer in demo mode. If an API key is configured in the server environment, requests are sent to the configured model provider. Do not enter sensitive or confidential text.</div></section>
<section class="card"><h2>Compare versions</h2><div class="outputs"><div><h3>Original <span class="tag">Source text</span></h3><div id="original" class="out">Your original text will appear here.</div></div><div><h3 id="resultHeading">Rewritten version</h3><div id="result" class="out">Your rewrite will appear here.</div></div><div id="secondBox" style="display:none"><h3>Formal and polished</h3><div id="second" class="out"></div></div><div id="factsBox" style="display:none"><h3>Source and interpretation</h3><div class="facts"><b>Information stated in source</b><div id="facts"></div></div><div class="interpret" style="margin-top:10px"><b>AI-generated interpretation</b><div id="interpretation"></div><div class="small">Interpretation is a generated summary and may infer meaning. Check it against the original.</div></div></div></div><p id="mode" class="small"></p></section><footer>Made by Group 3 · Eshita Chauhan, Divanshi Mittal, Vanshika Vats and Aymaan Dhingra</footer></main>
<script>
const $=id=>document.getElementById(id);$('go').addEventListener('click',async()=>{const text=$('source').value.trim();if(!text){$('status').textContent='Enter some text first.';return}const btn=$('go');btn.disabled=true;$('status').textContent='Working…';$('original').textContent=text;try{const r=await fetch('/rewrite',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,style:$('style').value,both:$('both').checked})});const d=await r.json();if(!r.ok)throw Error(d.error||'Request failed');$('result').textContent=d.primary;$('resultHeading').textContent=d.style==='formal'?'Formal and polished':'Clear and concise';$('secondBox').style.display=d.secondary?'block':'none';if(d.secondary)$('second').textContent=d.secondary;$('factsBox').style.display='grid';$('facts').textContent=d.facts.join('\n');$('interpretation').textContent=d.interpretation;$('mode').textContent='Mode: '+d.mode+' · Review the generated text before using it.';$('status').textContent='Done.'}catch(e){$('status').textContent=e.message}finally{btn.disabled=false}});
</script></body></html>'''

def local_rewrite(text, style):
    s = re.sub(r"\s+", " ", text.strip())
    s = re.sub(r"\bi\b", "I", s)
    s = re.sub(r"\b(the|a|an)\s+\1\b", r"\1", s, flags=re.I)
    s = re.sub(r"\s+([,.!?;:])", r"\1", s)
    s = re.sub(r"([.!?])(?=[A-Za-z])", r"\1 ", s)
    s = re.sub(r"\b(can't|cannot)\b", "cannot", s, flags=re.I)
    if style == "formal":
        for old, new in [(" don't ", " do not "), (" won't ", " will not "), (" it's ", " it is "), (" they're ", " they are "), (" gonna ", " going to ")]:
            s = s.replace(old, new).replace(old.title(), new)
        if s and s[-1] not in ".!?": s += "."
    else:
        if s and s[-1] not in ".!?": s += "."
    return s

def source_facts(text):
    # Extract source sentences as factual statements without adding new claims.
    pieces = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in pieces if p.strip()][:5]

def model_rewrite(text, style, both):
    prompt = ("You are a careful text editor. Rewrite only to improve grammar, clarity, and readability. "
              "Preserve every factual claim, uncertainty, number, and named entity. Do not add facts. "
              "Return JSON with keys primary, secondary, facts, interpretation. facts must list only claims explicitly stated in the source. "
              "interpretation must be a brief, clearly labeled inferred summary; if no inference is justified, say 'No additional interpretation.' "
              f"Primary style: {style}. Include a second style ('formal') only if both={str(both).lower()}. Source text:\n{text}")
    payload = {"model": MODEL, "temperature": 0.2, "messages": [{"role":"system","content":"Follow the requested JSON format."},{"role":"user","content":prompt}], "response_format":{"type":"json_object"}}
    req = Request(API_BASE + "/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization":"Bearer " + API_KEY,"Content-Type":"application/json"}, method="POST")
    with urlopen(req, timeout=45) as response:
        data=json.loads(response.read().decode())
    content=data["choices"][0]["message"]["content"]
    out=json.loads(content)
    return out

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404); return
        body=PAGE.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        if self.path != "/rewrite": self.send_error(404); return
        try:
            n=int(self.headers.get("Content-Length","0")); data=json.loads(self.rfile.read(n)); text=str(data.get("text",""))
            style=data.get("style","clear"); both=bool(data.get("both",True))
            if not text.strip(): raise ValueError("Text cannot be empty.")
            if len(text)>5000: raise ValueError("Please keep text to 5,000 characters or fewer.")
            if style not in ("clear","formal"): raise ValueError("Choose a supported style.")
            if API_KEY:
                result=model_rewrite(text,style,both); result["mode"]="AI model"; result["style"]=style
            else:
                primary=local_rewrite(text,style)
                result={"primary":primary,"secondary":local_rewrite(text,"formal") if both else "","facts":source_facts(text),"interpretation":"Demo mode does not generate a separate interpretation. The listed source sentences are extracted from the input; no new meaning has been inferred.","mode":"local demo rules","style":style}
            self.reply(200,result)
        except (ValueError,KeyError,json.JSONDecodeError) as e: self.reply(400,{"error":str(e)})
        except (HTTPError,URLError,TimeoutError) as e: self.reply(502,{"error":"Model request failed. Check the API endpoint, connection and credentials. " + str(e)})
        except Exception as e: self.reply(500,{"error":"Could not rewrite text: "+str(e)})
    def reply(self,status,obj):
        body=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self,fmt,*args): print("%s - %s"%(self.address_string(),fmt%args))

if __name__=="__main__":
    print(f"Assistant running at http://{HOST}:{PORT}")
    if not API_KEY: print("Demo mode: set OPENAI_API_KEY to enable an OpenAI-compatible model.")
    HTTPServer((HOST,PORT),Handler).serve_forever()
