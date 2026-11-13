# Rewrite Studio — Verification Notes

## Latest production deployment

| Check | Result | Notes |
|---|---|---|
| Build files | Passed | `npm run build` confirms the page and function files are present. |
| Production AI status | Passed | `/api/status` returns `ready: true` with `gpt-4o-mini`; no personal key is required. |
| Local preview page | Passed | `http://localhost:8888/` serves the Rewrite Studio page. |
| Local preview API connection | Passed | The browser app points localhost requests to the live Netlify functions. |
| Local preview CORS | Passed | Status returns HTTP 200 and rewrite preflight returns HTTP 204 for `http://localhost:8888`. |
| Live rewrite | Passed | A small sample rewrite succeeded through Netlify AI Gateway with no personal OpenAI key. |

Successful model requests use the Netlify team's AI credits. The app does not store drafts; they are sent to the model provider when a rewrite is requested.
