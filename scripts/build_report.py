#!/usr/bin/env python3
"""Render the editable report HTML to a short PDF without external services."""

from pathlib import Path

import pymupdf


def main():
    root = Path(__file__).resolve().parents[1]
    source = root / "docs/report.html"
    destination = root / "docs/report-draft.pdf"
    css = "body {font-family: sans-serif; font-size: 10pt; line-height: 1.35;} h1 {font-size: 22pt; color: #193c35;} h2 {font-size: 12pt; color: #226a4e; margin-top: 14pt;} p {margin: 7pt 0;}"
    story = pymupdf.Story(html=source.read_text(encoding="utf-8"), user_css=css)
    page = pymupdf.Rect(0, 0, 595, 842)
    content = pymupdf.Rect(42, 36, 553, 802)
    with pymupdf.DocumentWriter(str(destination)) as writer:
        more = True
        while more:
            device = writer.begin_page(page)
            more, _ = story.place(content)
            story.draw(device)
            writer.end_page()
    with pymupdf.open(destination) as document:
        print(f"Wrote {destination} ({len(document)} pages)")


if __name__ == "__main__":
    main()
