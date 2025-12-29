"""Free-source Q&A program.

This script answers a user question using free, public sources only.
It tries Wikipedia first, then DuckDuckGo search snippets, and falls back
to a short canned answer. No paid LLMs or external API keys are required.
"""
from dotenv import load_dotenv
import sys
import os

load_dotenv()

try:
    import wikipedia
except Exception:
    wikipedia = None

try:
    from duckduckgo_search import ddg
except Exception:
    ddg = None

def answer_wikipedia(query: str):
    if not wikipedia:
        return None, None
    try:
        hits = wikipedia.search(query)
        if not hits:
            return None, None
        page = wikipedia.page(hits[0], auto_suggest=False)
        # Return a short summary (first ~3 sentences)
        summary = "\n\n".join(page.summary.split('\n'))
        return summary, page.url
    except Exception:
        return None, None

def answer_duckduckgo(query: str):
    if not ddg:
        return None, None
    try:
        results = ddg(query, max_results=5)
        if not results:
            return None, None
        snippets = []
        for r in results:
            title = r.get('title') or r.get('text') or ''
            body = r.get('body') or r.get('snippet') or ''
            href = r.get('href') or r.get('url') or ''
            snippets.append(f"{title}: {body} ({href})")
        return "\n\n".join(snippets), results[0].get('href') or results[0].get('url')
    except Exception:
        return None, None

def canned_answer(query: str):
    return (
        "42 — a humorous/pop-culture answer from Douglas Adams. "
        "Different philosophies and religions propose their own meanings; "
        "explore ethics, relationships, creativity, and purpose for richer answers.",
        None,
    )

def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "what is the meaning of life?"

    answer, src = answer_wikipedia(query)
    source = 'wikipedia' if answer else None

    if not answer:
        answer, src = answer_duckduckgo(query)
        source = 'duckduckgo' if answer else None

    if not answer:
        answer, src = canned_answer(query)
        source = 'canned'

    print(f"Question: {query}\n")
    print("Answer:\n", answer)
    if src:
        print("\nSource:", src)


if __name__ == '__main__':
    main()