"""Convert a text-based PDF into a local Markdown artifact."""

from pathlib import Path
import logging
import time

import pymupdf
import pymupdf4llm

from research_library.files import atomic_write

logger = logging.getLogger(__name__)


def convert_pdf(source: Path, destination: Path) -> tuple[str, int]:
    started = time.monotonic()
    logger.info("PDF conversion started | paper=%s", source.name)
    with pymupdf.open(source) as document:
        pages = len(document)
        markdown = pymupdf4llm.to_markdown(document, show_progress=False)
    if not markdown.strip():
        raise ValueError("No text extracted; scanned PDFs need OCR, which is not configured.")
    atomic_write(destination, markdown)
    logger.info("PDF conversion finished | paper=%s | pages=%d | characters=%d | elapsed=%.2fs",
                source.name, pages, len(markdown), time.monotonic() - started)
    return markdown, pages
