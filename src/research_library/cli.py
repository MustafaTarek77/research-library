"""Local diagnostic runner; the scheduled deliverable is the Airflow DAG."""

import argparse
import logging
import os

from research_library.config import load_settings
from research_library.logging_utils import configure_logging
from research_library.notifications import notify_pending
from research_library.pipeline import convert, discover, generate_metadata, persist
from research_library.render import render_library
from research_library.storage import list_papers
from research_library.drive import download_papers, upload_html

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["run", "render", "status", "notify"], nargs="?", default="run")
    args = parser.parse_args()
    settings = load_settings()
    configure_logging(settings.log_file, os.getenv("LOG_LEVEL", "INFO"))
    if args.command == "status":
        papers = list_papers(settings.database_path)
        logger.info("Library status | stored=%d | pending_notifications=%d", len(papers), sum(p["notified_at"] is None for p in papers))
        return
    if args.command == "render":
        render_library(settings)
        return
    if args.command == "notify":
        render_library(settings)
        upload_html(settings)
        notify_pending(settings)
        return
    failures = []
    download_papers(settings)
    for paper in discover(settings):
        try:
            persist(generate_metadata(convert(paper, settings), settings), settings)
        except Exception:
            logger.exception("Paper processing failed | paper=%s", paper["filename"])
            failures.append(paper["filename"])
    render_library(settings)
    upload_html(settings)
    notify_pending(settings)
    if failures:
        raise SystemExit(f"Failed papers: {', '.join(failures)}")
    logger.info("Pipeline run finished")


if __name__ == "__main__":
    main()
