"""Local Ollama HTTP client; native API exposes inference timing counters."""

import json
import logging
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from research_library.metadata import SCHEMA, SYSTEM_PROMPT, parse_metadata
from research_library.logging_utils import progress

logger = logging.getLogger(__name__)


def request_json(base_url: str, path: str, body: dict | None = None, timeout: int = 900) -> dict:
    request = Request(
        base_url.rstrip("/") + path,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Ollama HTTP {error.code}: {error.read().decode()}") from error
    except URLError as error:
        raise RuntimeError(f"Cannot reach Ollama at {base_url}: {error.reason}") from error
    if "error" in result:
        raise RuntimeError(result["error"])
    return result


def extract_metadata(
    markdown: str,
    *,
    base_url: str,
    model: str,
    context: int = 32768,
    threads: int = 8,
    max_output: int = 512,
    timeout: int = 900,
    progress_seconds: int = 15,
    temperature: float = 0,
    seed: int = 42,
    keep_alive: str = "5m",
    num_gpu: int = 0,
) -> tuple[dict, list[dict]]:
    # An estimate, not tokenization. Never silently clip the input for speed.
    estimated_tokens = (len(markdown) + len(SYSTEM_PROMPT)) / 3
    if estimated_tokens + max_output + 1024 > context:
        raise ValueError("Paper may exceed the context budget; use an explicit long-paper strategy.")
    attempts = []
    for attempt in range(2):
        retry_note = "\nPrevious output was invalid. Check all required fields and return valid JSON." if attempt else ""
        logger.info("LLM request started | model=%s | attempt=%d/2 | characters=%d", model, attempt + 1, len(markdown))
        started = time.monotonic()
        with progress(logger, f"LLM model={model} attempt={attempt + 1}", progress_seconds):
            response = request_json(
                base_url, "/api/chat",
                {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT + retry_note},
                        {"role": "user", "content": "Extract metadata from this paper:\n\n" + markdown},
                    ],
                    "format": SCHEMA,
                    "stream": False,
                    "keep_alive": keep_alive,
                    "options": {
                        "num_gpu": num_gpu, "num_ctx": context, "num_thread": threads,
                        "num_predict": max_output, "temperature": temperature, "seed": seed,
                    },
                },
                timeout=timeout,
            )
        attempts.append(response)
        logger.info("LLM response received | elapsed=%.2fs | prompt_tokens=%s | output_tokens=%s",
                    time.monotonic() - started, response.get("prompt_eval_count"), response.get("eval_count"))
        try:
            if response.get("done_reason") == "length":
                raise ValueError("Model reached its output limit")
            metadata = parse_metadata(response["message"]["content"])
            logger.info("JSON validation passed | title=%s", metadata["title"])
            return metadata, attempts
        except (ValueError, KeyError, TypeError) as error:
            logger.warning("JSON validation failed | attempt=%d/2 | reason=%s", attempt + 1, error)
            if attempt:
                raise ValueError("Invalid metadata after two model responses") from error
    raise AssertionError("Unreachable")
