# Architecture and implementation milestones

The primary deliverable follows the assignment's local structure. An optional
Colab runner can later reuse the processing modules; it is not part of the
current milestone or a replacement for Airflow evidence.

```text
Google Drive papers/ -- optional rclone download --> local papers/
             |
             v
Airflow standalone — one scheduled DAG
             |
       Discover new filenames
             |
       Convert PDF to Markdown ----> Local intermediate files
             |
       Request metadata -----------> Local Ollama server
             |                            |
             +<--------- JSON ------------+
             |
       Validate and save ----------> Local data/papers.db
             |
       Render searchable HTML -----> Local output/index.html
             |
       Optional rclone upload -----> Google Drive output/index.html
             |
       Send notification ----------> Discord webhook
```

## Decisions

- Python processing modules are separate from the DAG definition, so they can be
  tested and benchmarked without starting Airflow.
- The benchmark starts with Qwen 2.5 1.5B in Q4_K_M quantization. Model quality and
  speed must be measured before treating it as the final choice.
- Ollama's native HTTP API supplies JSON-schema output and timing counters.
  Requests explicitly select CPU inference and basic JSON validation remains in
  Python. A malformed response gets one additional attempt.
- Intermediate Markdown stays on local disk; future Airflow task handoffs use
  paths and small metadata values rather than whole documents.
- The assignment assumes unique filenames. The future database will use that
  uniqueness to avoid repeating successful processing.
- The application database and Airflow's execution state are different stores.
  Neither belongs in the synced folder.
- The final page is static HTML with browser-side filtering. No web application
  server is needed for the library.

## Current scope and next decisions

Implemented: PDF-to-Markdown conversion, local metadata extraction and validation,
CPU benchmarking, the scheduled Airflow DAG, SQLite persistence, searchable static
HTML, Discord delivery with pending checkpoints, and application progress logs.
Two scheduled local runs have executed successfully; see execution-evidence.md.

Google Drive is authenticated through a local rclone remote. Optional DAG tasks
download input PDFs and upload the generated page when DRIVE_SYNC_ENABLED=true.
Desktop-synced or local folders use the same workflow with that setting false.
No database or application-state files are transferred to Drive.

Pending external setup: the real Discord webhook and delivery verification,
GitHub repository URL, group members, and final report completion.

The DAG runs every five minutes with catchup disabled, one active run, and one
active task. It maps conversion, extraction, and storage per new PDF. HTML
publication runs after processing settles and reads committed SQLite records;
it can publish successful papers even when another paper failed. A failure
watcher depends on every other task, keeping the overall DAG failed if any
stage fails. On an empty scan, mapped stages are skipped and HTML/notification
tasks still execute, allowing publication and notification recovery.

Markdown and validated JSON are written atomically. Metadata checkpoints are
keyed by paper identity, source checksum, prompt/schema, model name, and context.
SQLite uniqueness makes a repeated save harmless. Notifications read the durable
pending queue only after HTML publication and mark successful delivery after
Discord confirms it. The source hash is checked before and after conversion.

The full paper is sent to the model with a generous context allocation; its
character-based input estimate is not an exact tokenizer. Oversized papers fail
explicitly under that estimate; an arbitrary-length chunking design and OCR are
outside the initial scope.

Notifications cannot be atomically committed with SQLite. The implementation
should track notification progress and document that ambiguous network failures
can still lead to duplicate messages.

## Documentation references

- [Airflow standalone quick start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- [Ollama model and quantization](https://ollama.com/library/qwen2.5:1.5b)
- [Ollama native chat API](https://docs.ollama.com/api/chat)
- [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM)

The PDF converter is pinned to `pymupdf4llm==0.0.27` and `pymupdf==1.26.7`.
The initially resolved `pymupdf4llm==2.0` distribution contained only package
metadata and no importable module in this environment. A pinned working API
avoids relying on that distribution.
