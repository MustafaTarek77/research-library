"""Task-sized operations shared by the DAG and a diagnostic CLI runner."""

import hashlib
import json
import logging
from pathlib import Path
import time

from research_library.config import Settings
from research_library.files import atomic_write
from research_library.llm import extract_metadata
from research_library.metadata import SCHEMA, SYSTEM_PROMPT, parse_metadata
from research_library.storage import known_filenames, save_paper

logger = logging.getLogger(__name__)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discover(settings: Settings) -> list[dict]:
    if not settings.papers_dir.is_dir():
        raise FileNotFoundError(f"Papers directory is missing: {settings.papers_dir}")
    known = known_filenames(settings.database_path)
    pending = []
    skipped = 0
    logger.info("Discovery started | folder=%s | already_processed=%d", settings.papers_dir, len(known))
    for source in sorted(settings.papers_dir.iterdir()):
        if not source.is_file() or source.suffix.lower() != ".pdf":
            continue
        if source.name in known:
            logger.info("Paper skipped | paper=%s | reason=already_processed", source.name)
            skipped += 1
            continue
        stat = source.stat()
        if stat.st_size == 0 or time.time() - stat.st_mtime < settings.stability_seconds:
            logger.info("Paper deferred | paper=%s | reason=empty_or_recently_modified", source.name)
            continue
        pending.append({"filename": source.name, "pdf_path": str(source), "source_sha256": file_digest(source)})
    logger.info("Discovery finished | new=%d | skipped=%d", len(pending), skipped)
    return pending


def convert(paper: dict, settings: Settings) -> dict:
    from research_library.pdf import convert_pdf

    source = Path(paper["pdf_path"])
    if file_digest(source) != paper["source_sha256"]:
        raise ValueError("PDF changed after discovery; retry after sync finishes")
    identity = hashlib.sha256((paper["filename"] + paper["source_sha256"]).encode()).hexdigest()
    destination = settings.work_dir / "markdown" / f"{identity}.md"
    if destination.exists():
        logger.info("Markdown checkpoint reused | paper=%s", paper["filename"])
    else:
        convert_pdf(source, destination)
    if file_digest(source) != paper["source_sha256"]:
        destination.unlink(missing_ok=True)
        raise ValueError("PDF changed during conversion; retry after sync finishes")
    return paper | {"markdown_path": str(destination)}


def generate_metadata(paper: dict, settings: Settings) -> dict:
    checkpoint_key = hashlib.sha256(json.dumps({
        "paper": paper, "model": settings.model, "context": settings.context,
        "prompt": SYSTEM_PROMPT, "schema": SCHEMA,
        "generation": {"max_output": settings.max_output, "temperature": settings.temperature, "seed": settings.seed},
    }, sort_keys=True).encode()).hexdigest()
    destination = settings.work_dir / "metadata" / f"{checkpoint_key}.json"
    if destination.exists():
        parse_metadata(destination.read_text())
        logger.info("Metadata checkpoint reused | paper=%s", paper["filename"])
    else:
        logger.info("Metadata extraction started | paper=%s", paper["filename"])
        metadata, _ = extract_metadata(
            Path(paper["markdown_path"]).read_text(encoding="utf-8"),
            base_url=settings.base_url, model=settings.model, context=settings.context,
            threads=settings.threads, timeout=settings.timeout, progress_seconds=settings.progress_seconds,
            max_output=settings.max_output, temperature=settings.temperature, seed=settings.seed,
            keep_alive=settings.keep_alive, num_gpu=settings.num_gpu,
        )
        atomic_write(destination, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
        logger.info("Metadata checkpoint saved | paper=%s", paper["filename"])
    return paper | {"metadata_path": str(destination)}


def persist(paper: dict, settings: Settings) -> str:
    metadata = parse_metadata(Path(paper["metadata_path"]).read_text(encoding="utf-8"))
    inserted = save_paper(settings.database_path, paper["filename"], paper["source_sha256"], metadata)
    logger.info("SQLite commit | paper=%s | inserted=%s", paper["filename"], inserted)
    return paper["filename"]
