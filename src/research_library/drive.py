"""Non-deleting Drive transfers around the local processing pipeline."""

import logging
import os
import shutil
import subprocess

from research_library.config import Settings
from research_library.logging_utils import progress

logger = logging.getLogger(__name__)


def _run(settings: Settings, operation: str, arguments: list[str]) -> None:
    executable = shutil.which(settings.rclone_binary)
    if not executable:
        raise RuntimeError("rclone is not installed or not on PATH; install it or set RCLONE_BINARY")
    environment = os.environ.copy()
    if settings.rclone_config is not None:
        environment["RCLONE_CONFIG"] = str(settings.rclone_config)
    command = [executable, *arguments, "--contimeout", "15s", "--timeout", "60s",
               "--retries", "2", "--low-level-retries", "2"]
    logger.info("Drive %s started | remote=%s", operation, settings.rclone_remote)
    try:
        with progress(logger, f"Drive {operation}", settings.progress_seconds):
            result = subprocess.run(command, env=environment, capture_output=True, text=True,
                                    timeout=settings.drive_timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Drive {operation} exceeded DRIVE_SYNC_TIMEOUT_SECONDS") from None
    except OSError:
        raise RuntimeError(f"Could not start rclone for Drive {operation}") from None
    if result.returncode:
        # Do not forward raw subprocess output: OAuth errors may contain credentials.
        output = (result.stdout + result.stderr).lower()
        if "invalid_grant" in output:
            reason = "Google authorization expired or was revoked; reconnect the rclone remote"
        elif "accessnotconfigured" in output or "service_disabled" in output:
            reason = "Google Drive API must be enabled for the OAuth project"
        elif "directory not found" in output:
            reason = "the configured Drive folder was not found"
        else:
            reason = "check the rclone connection, folder path, and Google permissions"
        raise RuntimeError(f"Drive {operation} failed (rclone exit {result.returncode}): {reason}")
    logger.info("Drive %s finished", operation)


def download_papers(settings: Settings) -> bool:
    if not settings.drive_sync_enabled:
        logger.info("Drive download disabled | using local/desktop-synced folder")
        return False
    settings.papers_dir.mkdir(parents=True, exist_ok=True)
    _run(settings, "PDF download", ["copy", settings.rclone_remote + "/papers", str(settings.papers_dir),
                                    "--include", "*.pdf", "--ignore-case", "--max-depth", "1"])
    count = sum(path.is_file() and path.suffix.lower() == ".pdf" for path in settings.papers_dir.iterdir())
    logger.info("Local PDF folder ready | files=%d | path=%s", count, settings.papers_dir)
    return True


def upload_html(settings: Settings) -> bool:
    if not settings.drive_sync_enabled:
        logger.info("Drive upload disabled | HTML available in local/desktop-synced folder")
        return False
    source = settings.output_dir / "index.html"
    if not source.is_file():
        raise FileNotFoundError(f"Generate the library page before uploading: {source}")
    _run(settings, "HTML upload", ["copyto", str(source), settings.rclone_remote + "/output/index.html"])
    return True
