import pytest
from types import SimpleNamespace

import main


def test_canned_answer_contains_42():
    ans, src = main.canned_answer("anything")
    assert "42" in ans
    assert src is None


def test_answer_wikipedia_success(monkeypatch):
    # Mock wikipedia module functions
    page_obj = SimpleNamespace(summary="A short summary.", url="http://example.com")

    def fake_search(q):
        return ["Hit"]

    def fake_page_func(title, auto_suggest=False):
        return page_obj

    monkeypatch.setattr(main, 'wikipedia', SimpleNamespace(search=fake_search, page=fake_page_func))
    ans, url = main.answer_wikipedia("query")
    assert ans is not None and "short summary" in ans.lower()
    assert url == "http://example.com"


def test_answer_wikipedia_no_wikipedia(monkeypatch):
    monkeypatch.setattr(main, 'wikipedia', None)
    ans, url = main.answer_wikipedia("q")
    assert ans is None and url is None


def test_answer_duckduckgo_success(monkeypatch):
    sample = [{"title": "T", "body": "B", "href": "http://h"}]
    monkeypatch.setattr(main, 'ddg', lambda q, max_results=5: sample)
    ans, url = main.answer_duckduckgo("q")
    assert "T" in ans
    assert url == "http://h"


def test_answer_duckduckgo_no_ddg(monkeypatch):
    monkeypatch.setattr(main, 'ddg', None)
    ans, url = main.answer_duckduckgo('q')
    assert ans is None and url is None
