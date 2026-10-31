from dataclasses import replace
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from research_library.config import Settings, load_settings
from research_library.drive import download_papers, upload_html


@pytest.fixture
def settings(tmp_path):
    return Settings(papers_dir=tmp_path / "library/papers", output_dir=tmp_path / "library/output",
                    database_path=tmp_path / "data/papers.db", work_dir=tmp_path / "data",
                    log_file=tmp_path / "logs/pipeline.log", drive_sync_enabled=True,
                    rclone_config=tmp_path / "private/rclone.conf")


def test_desktop_mode_does_not_invoke_rclone(settings, monkeypatch):
    monkeypatch.setattr("research_library.drive.subprocess.run", lambda *a, **k: pytest.fail("Unexpected transfer"))
    local = replace(settings, drive_sync_enabled=False)
    assert not download_papers(local)
    assert not upload_html(local)


def test_download_is_scoped_non_deleting_and_pdf_only(settings, monkeypatch):
    requests = []
    monkeypatch.setattr("research_library.drive.shutil.which", lambda name: "/usr/bin/rclone")

    def fake_run(command, **kwargs):
        requests.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr("research_library.drive.subprocess.run", fake_run)
    assert download_papers(settings)
    command, options = requests[0]
    assert command[:4] == ["/usr/bin/rclone", "copy", "gdrive:ResearchLibrary/papers", str(settings.papers_dir)]
    assert command[command.index("--include") + 1] == "*.pdf"
    assert "--ignore-case" in command
    assert command[command.index("--max-depth") + 1] == "1"
    assert "sync" not in command and "--delete-excluded" not in command
    assert options["env"]["RCLONE_CONFIG"] == str(settings.rclone_config)


def test_upload_sends_only_generated_html(settings, monkeypatch):
    settings.output_dir.mkdir(parents=True)
    page = settings.output_dir / "index.html"
    page.write_text("<html>Library</html>")
    requests = []
    monkeypatch.setattr("research_library.drive.shutil.which", lambda name: "/usr/bin/rclone")

    def fake_run(command, **kwargs):
        requests.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr("research_library.drive.subprocess.run", fake_run)
    assert upload_html(settings)
    assert requests[0][:4] == ["/usr/bin/rclone", "copyto", str(page), "gdrive:ResearchLibrary/output/index.html"]


def test_missing_html_does_not_start_upload(settings, monkeypatch):
    monkeypatch.setattr("research_library.drive.subprocess.run", lambda *a, **k: pytest.fail("Unexpected transfer"))
    with pytest.raises(FileNotFoundError, match="Generate the library page"):
        upload_html(settings)


def test_transfer_error_redacts_raw_oauth_details(settings, monkeypatch):
    monkeypatch.setattr("research_library.drive.shutil.which", lambda name: "/usr/bin/rclone")
    monkeypatch.setattr("research_library.drive.subprocess.run", lambda *a, **k: SimpleNamespace(
        returncode=1, stdout="", stderr="invalid_grant access_token=private-test-token"))
    with pytest.raises(RuntimeError) as failure:
        download_papers(settings)
    assert "expired or was revoked" in str(failure.value)
    assert "private-test-token" not in str(failure.value)


def test_transfer_timeout_fails_stage(settings, monkeypatch):
    monkeypatch.setattr("research_library.drive.shutil.which", lambda name: "/usr/bin/rclone")

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("rclone", 300)

    monkeypatch.setattr("research_library.drive.subprocess.run", timeout)
    with pytest.raises(RuntimeError, match="DRIVE_SYNC_TIMEOUT_SECONDS"):
        download_papers(settings)


def test_drive_account_root_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCH_LIBRARY_ROOT", str(tmp_path))
    monkeypatch.setenv("PAPERS_DIR", "library/papers")
    monkeypatch.setenv("OUTPUT_DIR", "library/output")
    monkeypatch.setenv("DATABASE_PATH", "data/papers.db")
    monkeypatch.setenv("DRIVE_SYNC_ENABLED", "true")
    monkeypatch.setenv("RCLONE_REMOTE", "gdrive:")
    with pytest.raises(ValueError, match="specific Drive folder"):
        load_settings()
