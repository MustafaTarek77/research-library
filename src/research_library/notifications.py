"""Discord delivery after publication; pending rows survive later retries."""

import json
import logging
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from research_library.config import Settings
from research_library.storage import list_papers, mark_notified

logger = logging.getLogger(__name__)


def send_webhook(url: str, paper: dict) -> None:
    # URLs and network exception messages can contain the webhook secret.
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query)) | {"wait": "true"}
    target = urlunsplit(parts._replace(query=urlencode(query)))
    payload = {"content": f"New paper processed: {paper['title']}\nCategory: {paper['category']}\nFile: {paper['filename']}"[:1900],
               "allowed_mentions": {"parse": []}}
    request = Request(target, data=json.dumps(payload).encode(), headers={
        "Content-Type": "application/json", "User-Agent": "ResearchLibrary/0.1"})
    try:
        with urlopen(request, timeout=30) as response:
            confirmation = json.load(response)
        if not confirmation.get("id"):
            raise RuntimeError("Discord did not confirm message creation")
    except HTTPError as error:
        raise RuntimeError(f"Discord delivery failed (HTTP {error.code}); notification remains pending") from None
    except (URLError, OSError, ValueError):
        raise RuntimeError("Discord delivery failed; notification remains pending") from None


def notify_pending(settings: Settings) -> int:
    pending = list_papers(settings.database_path, pending_only=True)
    if not settings.discord_enabled:
        logger.warning("Discord disabled | pending=%d | configure .env to enable delivery", len(pending))
        return 0
    sent = 0
    for paper in pending:
        logger.info("Discord sending | paper=%s", paper["filename"])
        send_webhook(settings.webhook_url, paper)
        mark_notified(settings.database_path, paper["filename"])
        sent += 1
        logger.info("Discord confirmed | paper=%s", paper["filename"])
    return sent
