import json

import pytest

from research_library.llm import extract_metadata
from research_library.metadata import parse_metadata

VALID = {"title": "A paper", "summary": "A factual summary", "keywords": ["systems"], "category": "Computing"}


@pytest.mark.parametrize("raw", ["not json", "[]", "null", '{"title": "Only a title"}'])
def test_rejects_invalid_metadata(raw):
    with pytest.raises(ValueError):
        parse_metadata(raw)


@pytest.mark.parametrize("field,value", [("title", 7), ("summary", ""), ("category", None), ("keywords", "systems"), ("keywords", [7])])
def test_rejects_wrong_field_types(field, value):
    with pytest.raises(ValueError):
        parse_metadata(json.dumps(VALID | {field: value}))


def test_retries_invalid_json_once(monkeypatch):
    replies = iter([{"message": {"content": "broken"}}, {"message": {"content": json.dumps(VALID)}}])
    calls = []

    def fake_request(*args, **kwargs):
        calls.append(args)
        return next(replies)

    monkeypatch.setattr("research_library.llm.request_json", fake_request)
    metadata, responses = extract_metadata("A paper", base_url="http://localhost", model="test")
    assert metadata == VALID
    assert len(responses) == len(calls) == 2


def test_stops_after_second_invalid_response(monkeypatch):
    calls = []

    def fake_request(*args, **kwargs):
        calls.append(args)
        return {"message": {"content": "broken"}}

    monkeypatch.setattr("research_library.llm.request_json", fake_request)
    with pytest.raises(ValueError, match="two model responses"):
        extract_metadata("A paper", base_url="http://localhost", model="test")
    assert len(calls) == 2


def test_rejects_likely_oversized_paper_before_request(monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail("Should reject before contacting the model")

    monkeypatch.setattr("research_library.llm.request_json", unexpected)
    with pytest.raises(ValueError, match="context budget"):
        extract_metadata("x" * 10000, base_url="http://localhost", model="test", context=2048)
