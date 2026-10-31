#!/usr/bin/env python3
"""Measure full PDF conversion and CPU metadata extraction without Airflow."""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from research_library.llm import extract_metadata, request_json
from research_library.pdf import convert_pdf
from research_library.logging_utils import configure_logging
from research_library.config import load_environment


def main() -> None:
    load_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--base-url", default=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435"))
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--context", type=int, default=int(os.getenv("LLM_CONTEXT", "32768")))
    parser.add_argument("--threads", type=int, default=int(os.getenv("LLM_THREADS", "8")))
    parser.add_argument("--timeout", type=int, default=int(os.getenv("LLM_TIMEOUT_SECONDS", "900")))
    parser.add_argument("--output", type=Path, default=Path("benchmarks/cpu-mapreduce.json"))
    args = parser.parse_args()
    configure_logging(Path("logs/benchmark.log"), os.getenv("LOG_LEVEL", "INFO"))
    if min(args.runs, args.context, args.threads, args.timeout) < 1:
        parser.error("runs, context, threads, and timeout must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "pdf": str(args.pdf),
        "pdf_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
        "model": args.model,
        "context": args.context,
        "threads": args.threads,
        "max_output_tokens": 512,
        "num_gpu": 0,
        "platform": platform.platform(),
        "cpu": subprocess.check_output(["lscpu"], text=True),
        "memory_before": Path("/proc/meminfo").read_text(),
        "packages": {p: version(p) for p in ("pymupdf", "pymupdf4llm")},
        "runs": [],
        "caveat": "Repeat runs reuse the identical prompt and may benefit from prompt caching. "
                  "Only the first run represents unloaded-model, uncached full-paper inference. "
                  "Timing excludes Airflow, SQLite, HTML, Discord, and model download. "
                  "Input budget uses an estimate; inspect server logs for truncation.",
    }

    def save() -> None:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    try:
        report["server"] = request_json(args.base_url, "/api/version")
        report["model_details"] = request_json(args.base_url, "/api/show", {"model": args.model})
        started = time.perf_counter()
        markdown, pages = convert_pdf(args.pdf, Path("data/markdown") / (args.pdf.stem + ".md"))
        report.update(pdf_pages=pages, markdown_characters=len(markdown),
                      conversion_seconds=time.perf_counter() - started)
        print(f"Converted {pages} pages, {len(markdown):,} characters in {report['conversion_seconds']:.2f}s", flush=True)
        # Explicitly unload before the first measured request. Do not evict other models.
        request_json(args.base_url, "/api/generate", {"model": args.model, "keep_alive": 0})
        save()
        for index in range(args.runs):
            label = "cold_model_uncached_paper" if index == 0 else "warm_model_repeated_paper"
            print(f"Run {index + 1}/{args.runs}: {label}", flush=True)
            started = time.perf_counter()
            metadata, responses = extract_metadata(
                markdown, base_url=args.base_url, model=args.model,
                context=args.context, threads=args.threads, timeout=args.timeout,
            )
            elapsed = time.perf_counter() - started
            metrics = []
            for response in responses:
                item = {key: value for key, value in response.items() if key != "message"}
                duration = response.get("eval_duration", 0) / 1e9
                item["output_tokens_per_second"] = response.get("eval_count", 0) / duration if duration else None
                metrics.append(item)
            loaded = request_json(args.base_url, "/api/ps")
            matching = [m for m in loaded.get("models", []) if m.get("name") == args.model or m.get("model") == args.model]
            if not matching:
                raise RuntimeError("Cannot verify loaded model execution details")
            if any(m.get("size_vram", 0) != 0 for m in matching):
                raise RuntimeError("GPU allocation detected; this is not a CPU-only benchmark")
            report["runs"].append({
                "label": label, "wall_seconds": elapsed, "attempts": len(responses),
                "metadata": metadata, "metrics": metrics, "loaded_models": loaded,
            })
            save()
            print(f"  {elapsed:.2f}s; {len(responses)} attempt(s); valid JSON; CPU verified", flush=True)
            print(f"  Title: {metadata['title']}", flush=True)
        report["status"] = "complete"
    except Exception as error:
        report.update(status="failed", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        save()
    print(f"Saved {args.output}", flush=True)


if __name__ == "__main__":
    main()
