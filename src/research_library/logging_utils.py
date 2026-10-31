"""Progress logs for CLI output and Airflow task log capture."""

from contextlib import contextmanager
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import threading
import time


def configure_logging(log_file: Path, level: str = "INFO") -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s | %(message)s")
    console = logging.StreamHandler()
    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    for handler in (console, file_handler):
        handler.setFormatter(formatter)
    logging.basicConfig(level=level.upper(), handlers=[console, file_handler], force=True)


@contextmanager
def progress(logger: logging.Logger, description: str, interval: int = 15):
    started = time.monotonic()
    finished = threading.Event()

    def heartbeat():
        while not finished.wait(interval):
            logger.info("%s | still running | elapsed=%.0fs", description, time.monotonic() - started)

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        yield
    finally:
        finished.set()
        thread.join(timeout=1)
