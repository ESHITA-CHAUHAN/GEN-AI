# Text Rewriting and Grammar Assistant

Group 3 Gen AI project: rewrite user-provided text for clarity, grammar, and readability. Compare the source with two styles and keep source statements separate from generated interpretation.

## Run locally

Requires Python 3 and no third-party packages.

```bash
python3 app.py
```

Open http://127.0.0.1:8000. Without a key, the app uses a simple local rules-based demo mode. This demonstrates the interface but is not a language model and may miss grammar errors.

## Optional model-backed mode

Configure an OpenAI-compatible endpoint in environment variables before running:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"
export OPENAI_BASE_URL="https://api.openai.com/v1"
python3 app.py
```

Do not commit API keys. Model mode sends entered text to the configured provider. Review generated text before use.

## Project files

- `app.py` — local web app and optional model integration
- `report.docx` — six-page technical report
- `presentation.pptx` — presentation and live demo guide
- `test-cases.md` — manual test plan and results
- `presentation-outline.md` — 5–10 minute speaking outline

Student details are in the report and slides. This repository is private.
