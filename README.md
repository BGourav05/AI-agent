# AI Agent (free-source mode)

This workspace contains a simple AI agent that answers questions using free sources (no paid LLMs required).

Files of interest:

- `main.py` — Free-source Q&A program: uses `wikipedia` then `duckduckgo_search`, then a canned fallback.
- `tools.py` — Utilities: `save_tool`, `search_tool`, and `wiki_tool`. Includes a fallback `Tool` wrapper for older LangChain versions.
- `tools_test.py` — Small runtime checks for the tools.
- `requirements.txt` — Python dependencies (install into a venv).
- `sample.env` — Template for secret keys (empty by default).

Quick start (Windows PowerShell):

```powershell
# from workspace root
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the free Q&A script:

```powershell
# default question
.\.venv\Scripts\python.exe main.py

# or provide a custom question
.\.venv\Scripts\python.exe main.py "who is Ada Lovelace"
```

Run the tools checks:

```powershell
.\.venv\Scripts\python.exe tools_test.py
```

Notes:
- If you plan to use LLM integrations (OpenAI/Anthropic), populate `.env` or `sample.env` with your API keys and update `main.py` accordingly. This project currently runs in a free-source mode to avoid quota and billing issues.
- `tools.py` includes a simple fallback `Tool` dataclass if the installed LangChain version doesn't export `Tool`.

- CI & Coverage badges

- ![CI](https://github.com/BGourav05/AI-agent/actions/workflows/ci.yml/badge.svg)  
- [![codecov](https://codecov.io/gh/BGourav05/AI-agent/branch/main/graph/badge.svg)](https://codecov.io/gh/BGourav05/AI-agent)  

Replace `OWNER/REPO` in the badge URLs with your repository owner and name.

If you want, I can:
- Switch `main.py` back to LLM-based mode and add config to choose provider (requires API keys).
- Add unit tests or GitHub Actions for CI.
- Create a small CLI wrapper to save outputs automatically.

Agent usage
-----------

This project includes a concise-answer interactive agent implemented in `agent.py`.
It answers questions using only free public sources (Wikipedia, DuckDuckGo) and returns
a short, easy-to-read response (1–2 sentences). Examples:

Interactive REPL:

```powershell
.\.venv\Scripts\Activate.ps1
python agent.py
# then type questions at the "Question:" prompt
```

Single-query mode:

```powershell
.\.venv\Scripts\Activate.ps1
python agent.py "what is photosynthesis?"
```

When to use which script:
- Use `main.py` for a fuller, longer answer with source excerpts.
- Use `agent.py` for brief, conversational answers suitable for quick responses.

If you'd like, I can add a small unit test for `agent.py` and a README example showing
how to invoke the agent programmatically from other scripts.
