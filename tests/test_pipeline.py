from dataclasses import replace
import json
from pathlib import Path

import pytest

from research_library.config import Settings, load_settings
from research_library.notifications import notify_pending, send_webhook
from research_library.pipeline import convert, discover, file_digest, generate_metadata, persist
from research_library.render import render_library
from research_library.storage import list_papers, save_paper

METADATA = {"title": "A distributed system", "summary": "A factual summary.",
            "keywords": ["systems", "data"], "category": "Data Engineering"}


@pytest.fixture
def settings(tmp_path):
    library = tmp_path / "ResearchLibrary"
    (library / "papers").mkdir(parents=True)
    return Settings(papers_dir=library / "papers", output_dir=library / "output",
                    database_path=tmp_path / "data/papers.db", work_dir=tmp_path / "data",
                    log_file=tmp_path / "logs/pipeline.log", stability_seconds=0)


def test_store_retry_does_not_duplicate_or_overwrite(settings):
    assert save_paper(settings.database_path, "paper.pdf", "digest", METADATA)
    assert not save_paper(settings.database_path, "paper.pdf", "digest", METADATA | {"title": "Changed"})
    rows = list_papers(settings.database_path)
    assert len(rows) == 1
    assert rows[0]["title"] == METADATA["title"]
    assert rows[0]["keywords"] == METADATA["keywords"]


def test_discovery_skips_processed_and_defers_unstable_files(settings):
    (settings.papers_dir / "old.pdf").write_bytes(b"pdf")
    (settings.papers_dir / "new.PDF").write_bytes(b"pdf")
    (settings.papers_dir / "empty.pdf").touch()
    (settings.papers_dir / "incomplete.pdf.part").write_bytes(b"partial")
    save_paper(settings.database_path, "old.pdf", "digest", METADATA)
    assert [p["filename"] for p in discover(settings)] == ["new.PDF"]
    assert discover(replace(settings, stability_seconds=3600)) == []


def test_retries_reuse_metadata_checkpoint(settings, monkeypatch):
    source = settings.papers_dir / "paper.pdf"
    source.write_bytes(b"input")
    markdown = settings.work_dir / "paper.md"
    markdown.parent.mkdir(parents=True)
    markdown.write_text("Paper contents")
    paper = {"filename": source.name, "pdf_path": str(source),
             "source_sha256": file_digest(source), "markdown_path": str(markdown)}
    calls = []

    def fake_model(*args, **kwargs):
        calls.append(1)
        return METADATA, []

    monkeypatch.setattr("research_library.pipeline.extract_metadata", fake_model)
    persist(generate_metadata(paper, settings), settings)
    persist(generate_metadata(paper, settings), settings)
    assert calls == [1]
    assert len(list_papers(settings.database_path)) == 1


def test_conversion_rejects_pdf_changed_since_discovery(settings):
    source = settings.papers_dir / "paper.pdf"
    source.write_bytes(b"original")
    paper = discover(settings)[0]
    source.write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed after discovery"):
        convert(paper, settings)


def test_publication_escapes_model_text_and_encodes_pdf_links(settings):
    metadata = METADATA | {"title": '<script>alert("x")</script>',
                           "summary": "<img src=x onerror=alert(1)> $cards",
                           "category": 'x" onclick="alert(1)', "keywords": ["<unsafe>"]}
    save_paper(settings.database_path, "paper #1.pdf", "digest", metadata)
    output = Path(render_library(settings)).read_text()
    assert '<script>alert("x")</script>' not in output
    assert "&lt;script&gt;" in output
    assert "&lt;img" in output
    assert "../papers/paper%20%231.pdf" in output
    assert "$cards" in output  # inserted data was not substituted a second time
    assert "&lt;unsafe&gt;" in output


def test_failed_notification_remains_pending_and_retry_avoids_reprocessing(settings, monkeypatch):
    save_paper(settings.database_path, "paper.pdf", "digest", METADATA)
    enabled = replace(settings, discord_enabled=True, webhook_url="https://example.invalid/secret")

    def fail(*args):
        raise RuntimeError("Temporary delivery failure")

    monkeypatch.setattr("research_library.notifications.send_webhook", fail)
    with pytest.raises(RuntimeError):
        notify_pending(enabled)
    assert len(list_papers(settings.database_path, pending_only=True)) == 1
    deliveries = []
    monkeypatch.setattr("research_library.notifications.send_webhook", lambda url, paper: deliveries.append(paper))
    assert notify_pending(enabled) == 1
    assert notify_pending(enabled) == 0
    assert len(deliveries) == 1


def test_disabled_notifications_preserve_queue(settings, monkeypatch):
    save_paper(settings.database_path, "paper.pdf", "digest", METADATA)
    monkeypatch.setattr("research_library.notifications.send_webhook", lambda *args: pytest.fail("Delivery disabled"))
    assert notify_pending(settings) == 0
    assert len(list_papers(settings.database_path, pending_only=True)) == 1


def test_webhook_confirmation_and_mentions(monkeypatch):
    import io
    captured = []

    def fake_http(request, timeout):
        captured.append(request)
        return io.BytesIO(b'{"id":"12345"}')

    monkeypatch.setattr("research_library.notifications.urlopen", fake_http)
    send_webhook("https://discord.com/api/webhooks/123/secret?thread_id=456", METADATA | {"filename": "paper.pdf"})
    request = captured[0]
    assert "wait=true" in request.full_url and "thread_id=456" in request.full_url
    assert json.loads(request.data)["allowed_mentions"] == {"parse": []}


def test_webhook_network_failure_does_not_expose_secret(monkeypatch):
    from urllib.error import URLError

    def fake_http(*args, **kwargs):
        raise URLError("https://discord.com/api/webhooks/123/secret")

    monkeypatch.setattr("research_library.notifications.urlopen", fake_http)
    with pytest.raises(RuntimeError) as failure:
        send_webhook("https://discord.com/api/webhooks/123/secret", METADATA | {"filename": "paper.pdf"})
    assert "secret" not in str(failure.value)


def test_database_cannot_live_in_synced_library(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCH_LIBRARY_ROOT", str(tmp_path))
    monkeypatch.setenv("PAPERS_DIR", "ResearchLibrary/papers")
    monkeypatch.setenv("OUTPUT_DIR", "ResearchLibrary/output")
    monkeypatch.setenv("DATABASE_PATH", "ResearchLibrary/papers.db")
    with pytest.raises(ValueError, match="outside ResearchLibrary"):
        load_settings()
