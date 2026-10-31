"""Configuration resolved at task execution time, not DAG import time."""

from dataclasses import dataclass, field
import os
from pathlib import Path, PureWindowsPath
import shutil
import subprocess

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_project_path(value: str, root: Path) -> Path:
    """Accept project-relative/Linux paths, and translate Windows paths in WSL."""
    windows = PureWindowsPath(value)
    if windows.drive and os.name != "nt":
        if not windows.is_absolute():
            raise ValueError("Use an absolute Windows path, for example C:/Users/name/ResearchLibrary/papers")
        converter = shutil.which("wslpath")
        if not converter:
            raise ValueError("Windows paths require WSL; use a Linux path in this environment")
        try:
            converted = subprocess.run([converter, "-u", value], check=True, capture_output=True,
                                       text=True, timeout=5).stdout.strip()
        except (subprocess.SubprocessError, OSError):
            raise ValueError("Cannot translate the Windows path; verify it is accessible from WSL") from None
        if not converted or not Path(converted).is_absolute():
            raise ValueError("Windows path translation did not return an absolute WSL path")
        return Path(converted).resolve()
    return (root / Path(value).expanduser()).resolve()


@dataclass(frozen=True)
class Settings:
    papers_dir: Path
    output_dir: Path
    database_path: Path
    work_dir: Path
    log_file: Path
    base_url: str = "http://127.0.0.1:11435"
    model: str = "qwen2.5:1.5b"
    context: int = 32768
    threads: int = 8
    timeout: int = 900
    progress_seconds: int = 15
    stability_seconds: int = 10
    max_output: int = 512
    temperature: float = 0
    seed: int = 42
    keep_alive: str = "5m"
    num_gpu: int = 0
    discord_enabled: bool = False
    webhook_url: str = field(default="", repr=False)
    drive_sync_enabled: bool = False
    rclone_remote: str = "gdrive:ResearchLibrary"
    rclone_config: Path | None = None
    rclone_binary: str = "rclone"
    drive_timeout: int = 300


def load_environment() -> Path:
    root = Path(os.getenv("RESEARCH_LIBRARY_ROOT", PROJECT_ROOT)).expanduser().resolve()
    load_dotenv(root / ".env", override=False, interpolate=False)
    return root


def load_settings() -> Settings:
    root = load_environment()

    def path(key, default):
        return resolve_project_path(os.getenv(key, default), root)

    def positive(key, default, allow_zero=False):
        value = int(os.getenv(key, str(default)))
        if value < (0 if allow_zero else 1):
            raise ValueError(f"Invalid value for {key}")
        return value

    settings = Settings(
        papers_dir=path("PAPERS_DIR", "ResearchLibrary/papers"),
        output_dir=path("OUTPUT_DIR", "ResearchLibrary/output"),
        database_path=path("DATABASE_PATH", "data/papers.db"),
        work_dir=path("WORK_DIR", "data"), log_file=path("LOG_FILE", "logs/pipeline.log"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435"),
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"),
        context=positive("LLM_CONTEXT", 32768), threads=positive("LLM_THREADS", 8),
        timeout=positive("LLM_TIMEOUT_SECONDS", 900), progress_seconds=positive("LLM_PROGRESS_SECONDS", 15),
        stability_seconds=positive("FILE_STABILITY_SECONDS", 10, allow_zero=True),
        max_output=positive("LLM_MAX_OUTPUT_TOKENS", 512),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0")),
        seed=int(os.getenv("LLM_SEED", "42")),
        keep_alive=os.getenv("LLM_KEEP_ALIVE", "5m"),
        num_gpu=int(os.getenv("LLM_NUM_GPU", "0")),
        discord_enabled=os.getenv("DISCORD_ENABLED", "false").lower() == "true",
        webhook_url=os.getenv("DISCORD_WEBHOOK_URL", ""),
        drive_sync_enabled=os.getenv("DRIVE_SYNC_ENABLED", "false").lower() == "true",
        rclone_remote=os.getenv("RCLONE_REMOTE", "gdrive:ResearchLibrary").rstrip("/"),
        rclone_config=path("RCLONE_CONFIG", "data/rclone/rclone.conf"),
        rclone_binary=os.getenv("RCLONE_BINARY", "rclone"),
        drive_timeout=positive("DRIVE_SYNC_TIMEOUT_SECONDS", 300),
    )
    library_root = settings.papers_dir.parent
    if settings.output_dir == settings.papers_dir:
        raise ValueError("Papers and output must be separate directories")
    if settings.output_dir.parent != library_root:
        raise ValueError("papers/ and output/ must share a ResearchLibrary parent")
    for local_path in (settings.database_path, settings.work_dir, settings.log_file):
        if local_path.is_relative_to(library_root):
            raise ValueError("Database, work files, and logs must stay outside ResearchLibrary")
    if settings.discord_enabled and not settings.webhook_url:
        raise ValueError("DISCORD_ENABLED=true requires DISCORD_WEBHOOK_URL")
    if settings.drive_sync_enabled:
        remote, separator, folder = settings.rclone_remote.partition(":")
        if not remote or not separator or not folder.strip("/") or any(part in (".", "..") for part in folder.split("/")):
            raise ValueError("RCLONE_REMOTE must name a specific Drive folder, for example gdrive:ResearchLibrary")
        if settings.rclone_config.is_relative_to(library_root):
            raise ValueError("The rclone token config must stay outside ResearchLibrary")
    return settings
