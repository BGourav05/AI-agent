import agent


def test_answer_query_prefers_wikipedia(monkeypatch):
    # Wikipedia returns a long multi-sentence summary and a URL
    monkeypatch.setattr(agent, 'answer_wikipedia', lambda q: (
        "This is the first sentence. This is the second sentence. More details follow.",
        "https://example.org/wiki"
    ))
    monkeypatch.setattr(agent, 'answer_duckduckgo', lambda q: (None, None))

    ans, src = agent.answer_query("some query")
    assert isinstance(ans, str) and len(ans) > 0
    assert src == "https://example.org/wiki"
    # Brief should contain at most two sentences
    assert ans.count('.') <= 2


def test_answer_query_falls_back_to_duckduckgo(monkeypatch):
    monkeypatch.setattr(agent, 'answer_wikipedia', lambda q: (None, None))
    monkeypatch.setattr(agent, 'answer_duckduckgo', lambda q: (
        "Result title: snippet text explaining the topic.",
        "https://example.org/search"
    ))

    ans, src = agent.answer_query("other query")
    assert isinstance(ans, str) and len(ans) > 0
    assert src == "https://example.org/search"


def test_answer_query_uses_canned_when_none(monkeypatch):
    monkeypatch.setattr(agent, 'answer_wikipedia', lambda q: (None, None))
    monkeypatch.setattr(agent, 'answer_duckduckgo', lambda q: (None, None))

    ans, src = agent.answer_query("unknown query")
    assert isinstance(ans, str) and len(ans) > 0
    assert src == "canned"
