"""Interactive concise-answer AI agent (free-source).

Runs in an interactive REPL or answers a single query passed as CLI args.
It tries Wikipedia first, then DuckDuckGo, and falls back to a canned reply.
Answers are shortened to 1-2 sentences for brief, easy-to-read responses.
"""
from __future__ import annotations
import re
import sys
from typing import Optional

try:
    from main import answer_wikipedia, answer_duckduckgo, canned_answer
except Exception:
    # If importing fails, fallback to local implementations copied lightly
    from main import answer_wikipedia, answer_duckduckgo, canned_answer  # re-raise for visibility


def briefify(text: str, max_sentences: int = 2) -> str:
    if not text:
        return ""
    # Remove bracketed references like [1], (citation needed)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\(citation needed\)", "", text, flags=re.IGNORECASE)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Split into sentences
    parts = re.split(r'(?<=[.!?])\s+', text)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 0:
        return text[:300]
    brief = " ".join(parts[:max_sentences])
    if len(brief) > 600:
        # hard truncate while preserving words
        brief = brief[:600].rsplit(" ", 1)[0] + "..."
    return brief


def answer_query(query: str) -> tuple[str, Optional[str]]:
    # Try Wikipedia
    ans, src = answer_wikipedia(query)
    if ans:
        return briefify(ans, 2), src or "wikipedia"

    # Try DuckDuckGo
    ans, src = answer_duckduckgo(query)
    if ans:
        return briefify(ans, 2), src or "duckduckgo"

    # Fallback
    ans, src = canned_answer(query)
    return briefify(ans, 2), src or "canned"


def repl():
    print("Interactive concise-answer agent. Type 'exit' or Ctrl-C to quit.")
    try:
        while True:
            q = input('\nQuestion: ').strip()
            if not q:
                continue
            if q.lower() in ("exit", "quit"):
                print("Goodbye.")
                break
            ans, src = answer_query(q)
            print('\nAnswer (brief):')
            print(ans)
            if src:
                print('\nSource:', src)
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting.')


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        ans, src = answer_query(query)
        print(f"Question: {query}\n")
        print("Answer (brief):")
        print(ans)
        if src:
            print("\nSource:", src)
        return
    repl()


if __name__ == '__main__':
    main()
