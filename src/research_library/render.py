"""Generate a self-contained static page from committed SQLite records."""

from html import escape
from importlib.resources import files
import logging
import os
from urllib.parse import quote

from research_library.config import Settings
from research_library.files import atomic_write
from research_library.storage import list_papers, timestamp

logger = logging.getLogger(__name__)


def render_library(settings: Settings) -> str:
    papers = list_papers(settings.database_path)
    cards = []
    for paper in papers:
        keywords = "".join(f'<span class="tag">{escape(word)}</span>' for word in paper["keywords"])
        relative_folder = os.path.relpath(settings.papers_dir, settings.output_dir)
        link = quote(relative_folder, safe="/") + "/" + quote(paper["filename"], safe="")
        cards.append(f'''<article class="paper" data-category="{escape(paper['category'], quote=True)}">
          <div class="category">{escape(paper['category'])}</div>
          <h2><a href="{escape(link, quote=True)}" target="_blank" rel="noopener">{escape(paper['title'])}</a></h2>
          <p class="summary">{escape(paper['summary'])}</p>
          <div class="tags">{keywords}</div>
          <div class="paper-footer"><span>{escape(paper['filename'])}</span><a href="{escape(link, quote=True)}" target="_blank" rel="noopener">Open PDF ↗</a></div>
        </article>''')
    options = "".join(f'<option value="{escape(category, quote=True)}">{escape(category)}</option>'
                      for category in sorted({paper["category"] for paper in papers}))
    template = files("research_library").joinpath("templates/library.html").read_text(encoding="utf-8")
    # Single-pass substitution: model text can never be interpreted as a template token.
    from string import Template
    html = Template(template).substitute(cards="\n".join(cards), categories=options,
                                         count=len(papers), generated=escape(timestamp()))
    destination = settings.output_dir / "index.html"
    atomic_write(destination, html)
    logger.info("HTML published | papers=%d | path=%s", len(papers), destination)
    return str(destination)
