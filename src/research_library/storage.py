"""One record per unique filename, plus notification checkpoints."""

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connect(database: Path):
    database.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(database, timeout=30)
    db.row_factory = sqlite3.Row
    try:
        with db:
            db.execute("""CREATE TABLE IF NOT EXISTS papers (
                filename TEXT PRIMARY KEY, title TEXT NOT NULL, summary TEXT NOT NULL,
                keywords TEXT NOT NULL, category TEXT NOT NULL, source_sha256 TEXT NOT NULL,
                processed_at TEXT NOT NULL, notified_at TEXT
            )""")
            yield db
    finally:
        db.close()


def known_filenames(database: Path) -> set[str]:
    with connect(database) as db:
        return {row[0] for row in db.execute("SELECT filename FROM papers")}


def save_paper(database: Path, filename: str, digest: str, metadata: dict) -> bool:
    with connect(database) as db:
        result = db.execute("""INSERT INTO papers
            (filename, title, summary, keywords, category, source_sha256, processed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(filename) DO NOTHING""",
            (filename, metadata["title"], metadata["summary"], json.dumps(metadata["keywords"]),
             metadata["category"], digest, timestamp()))
        return result.rowcount == 1


def list_papers(database: Path, *, pending_only: bool = False) -> list[dict]:
    with connect(database) as db:
        query = "SELECT * FROM papers"
        if pending_only:
            query += " WHERE notified_at IS NULL"
        rows = db.execute(query + " ORDER BY processed_at DESC, filename").fetchall()
        return [dict(row) | {"keywords": json.loads(row["keywords"])} for row in rows]


def mark_notified(database: Path, filename: str) -> None:
    with connect(database) as db:
        db.execute("UPDATE papers SET notified_at = ? WHERE filename = ?", (timestamp(), filename))
