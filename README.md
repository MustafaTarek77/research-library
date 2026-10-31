# Research Paper Library

A local pipeline for organizing research papers. Apache Airflow schedules the
workflow, PyMuPDF4LLM converts PDFs to Markdown, and Ollama generates a title,
summary, keywords, and category for each paper. The metadata is stored in SQLite
and published as a searchable HTML library.

## Workflow

```text
Download from Drive -> Discover new PDFs -> Convert to Markdown -> Generate JSON
                                                               |
                                                               v
                                                           SQLite
                                                               |
                                                               v
                                                        Generate HTML
                                                               |
                                                               v
                                                        Upload to Drive
                                                               |
                                                               v
                                                        Notify Discord
```

The `paper_pipeline` DAG runs every five minutes by default. Conversion,
extraction, and storage are mapped per paper. One task runs at a time to keep CPU
and memory usage manageable during inference.

Each paper is identified by its filename. Successfully stored papers are skipped
on later runs. Markdown and metadata checkpoints allow retries to reuse completed
work. HTML is rebuilt from committed records, so successful papers can still be
published if another paper fails. A failure watcher keeps the DAG marked as
failed when any processing stage fails.

## Requirements

- Python 3.12
- Linux or Ubuntu through WSL2 on Windows
- Ollama
- Google Drive for desktop or rclone for Drive transfers
- A Discord webhook to enable notifications

The default model is `qwen2.5:1.5b` with Q4_K_M quantization. It runs on the CPU;
no GPU or cloud LLM API is required.

## Installation

Run these commands from the project directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
bash scripts/setup_airflow.sh
cp .env.example .env
```

Skip the last command if `.env` already exists.

There are two Python environments:

| Environment | Purpose |
| --- | --- |
| `.venv` | Tests, benchmarks, and manual pipeline commands |
| `.airflow-venv` | Airflow 3.3.2 and scheduled task execution |

The Airflow setup script uses the official Python 3.12 constraints file. Both
environments use the same application source under `src/research_library/`.

## Configuration

Settings are grouped in `.env`; `.env.example` lists the defaults. The startup
scripts and application load this file automatically. Exported shell variables
take precedence. Relative paths are resolved against the project directory.
Restart the affected services from fresh terminals after changing settings.

| Settings | Purpose |
| --- | --- |
| `PAPERS_DIR`, `OUTPUT_DIR` | Input PDFs and generated HTML |
| `DATABASE_PATH`, `WORK_DIR` | Local database and intermediate files |
| `LLM_*` | Context size, threads, output limit, generation settings, and timeout |
| `OLLAMA_*` | Model, server address, model cache, and server limits |
| `PIPELINE_*` | Schedule, concurrency, retry delay, and task timeout |
| `AIRFLOW_*` | Airflow state, DAG folder, and standalone settings |
| `LOG_*`, `FILE_STABILITY_SECONDS` | Logging and file discovery |
| `DISCORD_*` | Webhook URL and notification switch |
| `DRIVE_SYNC_*`, `RCLONE_*` | Optional Google Drive transfers and connection settings |

Keep `.env`, OAuth tokens, and generated credentials out of version control.

## Running the pipeline

Start Ollama in one terminal:

```bash
bash scripts/serve_cpu.sh
```

In another terminal, load the configuration, download the model, and start Airflow:

```bash
source scripts/load_env.sh
ollama pull "$OLLAMA_MODEL"
bash scripts/start_airflow.sh
```

The default addresses are:

- Airflow: http://localhost:8080
- Ollama: http://127.0.0.1:11435

Log in to Airflow as `admin`. The generated password is stored in
`.airflow/simple_auth_manager_passwords.json.generated`.

Enable `paper_pipeline` in the dashboard. To enable it from the terminal:

```bash
source scripts/airflow_env.sh
airflow dags unpause paper_pipeline
```

Place PDFs directly in `ResearchLibrary/papers/`, or the configured `PAPERS_DIR`.
Wait at least ten seconds after copying a file before triggering a run. Files
that are empty or recently modified are deferred to a later scan.

Trigger a run immediately with:

```bash
source scripts/airflow_env.sh
airflow dags trigger paper_pipeline
```

After processing, open `ResearchLibrary/output/index.html` in a browser. The page
supports text search and category filtering, with relative links to the source
PDFs. Refresh the page after a new run finishes.

To stop the services, pause the DAG and press Ctrl+C in the Airflow and Ollama
terminals.

## Google Drive

The synced library contains only the input PDFs and generated page:

```text
ResearchLibrary/
|-- papers/
+-- output/
    +-- index.html
```

Keep `data/`, `.airflow/`, logs, and model weights outside this directory.
`data/papers.db` stores paper metadata; `.airflow/airflow.db` stores workflow
execution history. They are separate databases.

### Google Drive for desktop

Point `PAPERS_DIR` and `OUTPUT_DIR` at locally available, synced folders.
Windows paths are supported when running through WSL:

```dotenv
PAPERS_DIR='C:\Users\username\My Drive\ResearchLibrary\papers'
OUTPUT_DIR='C:\Users\username\My Drive\ResearchLibrary\output'
```

Equivalent `/mnt/c/...` paths also work. Use single quotes around Windows paths
with backslashes. The drive must be accessible from WSL; path conversion does
not mount a Windows virtual drive. No rclone credentials are needed for this
setup.

### Rclone in WSL

Rclone can transfer files between Drive and the local library. Configure a Google
Drive remote named `gdrive`. OAuth client settings belong in `.env`, and the
local token configuration is stored at `data/rclone/rclone.conf`.

After authorization, run transfers from the project directory:

```bash
source scripts/load_env.sh

# Download PDFs before processing.
rclone copy gdrive:ResearchLibrary/papers "$PAPERS_DIR"

# Upload the generated page after processing.
rclone copyto "$OUTPUT_DIR/index.html" gdrive:ResearchLibrary/output/index.html
```

To make these transfers part of every DAG run, configure:

```dotenv
DRIVE_SYNC_ENABLED=true
RCLONE_REMOTE="gdrive:ResearchLibrary"
RCLONE_CONFIG="./data/rclone/rclone.conf"
RCLONE_BINARY=rclone
DRIVE_SYNC_TIMEOUT_SECONDS=300
```

Restart Airflow from a fresh terminal. `download_drive_pdfs` downloads PDFs from
the remote `papers/` folder before discovery. `upload_drive_html` uploads only
`output/index.html` after generation and before Discord delivery. Transfers use
`copy` and `copyto`, leaving unrelated destination files in place. No database,
model, log, or token files are uploaded. Subdirectories under `papers/` are not
scanned or downloaded. Local PDFs are not automatically uploaded to Drive; add
them to the remote `papers/` folder if they should be available there as well.

A failed input transfer blocks the upload and notification stages. An upload
failure leaves notifications pending for a later run. Transfers have bounded
timeouts and emit progress heartbeats in Airflow logs. The page is also uploaded
on runs with no new PDFs, allowing recovery after a previous upload failure.

For Google Drive for desktop or local-only use, leave `DRIVE_SYNC_ENABLED=false`.
Both transfer tasks then complete without invoking rclone or requiring OAuth.

## Discord notifications

Create an incoming webhook for a Discord text channel and set:

```dotenv
DISCORD_ENABLED=true
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/WEBHOOK_ID/WEBHOOK_TOKEN"
```

Notifications are disabled by default. When enabled, the final task sends one
message per pending paper and records confirmation in SQLite. Failed or disabled
delivery stays pending for a later run.

To publish the page and send pending notifications manually:

```bash
.venv/bin/research-library notify
```

A failure after Discord accepts a message but before the database records it can
cause a duplicate on retry. Webhook URLs are excluded from application logs.

## Logs and troubleshooting

Follow application progress from a separate terminal:

```bash
.venv/bin/python scripts/show_progress.py
```

Add `--once` to print existing events and exit. LLM requests emit a heartbeat
every 15 seconds while waiting for a response.

In Airflow, select a DAG run, click a task, and open its logs. Start with
`discover_pdfs` if a paper is not picked up. A successful discovery task can
return zero new files, causing conversion, extraction, and storage to be skipped.
A skipped `report_failure` task is expected on successful runs.

| Location | Contents |
| --- | --- |
| `.airflow/logs/` | Airflow task and scheduler logs |
| `logs/pipeline.log` | Manual pipeline logs |
| `logs/benchmark.log` | CPU benchmark logs |
| `data/markdown/` | Converted text |
| `data/metadata/` | Validated JSON checkpoints |

Useful commands:

```bash
source scripts/airflow_env.sh
airflow dags list-import-errors --output json
airflow dags list-runs paper_pipeline --output table
.venv/bin/research-library status
```

## Tests and benchmarks

```bash
.venv/bin/python -m pytest -q
```

Tests cover JSON validation and retries, duplicate prevention, checkpoint reuse,
source changes, HTML escaping, notification recovery, environment loading, and
Windows path conversion in WSL.

To benchmark a paper independently of Airflow:

```bash
.venv/bin/python scripts/benchmark_cpu.py ResearchLibrary/papers/paper.pdf --runs 3
```

The benchmark saves timings and generated metadata under `benchmarks/`. The
[CPU benchmark results](docs/cpu-benchmark.md) include the hardware, model settings,
and cache behavior. Cached repeat requests are not representative of processing
a new paper.

For a sequential diagnostic run:

```bash
.venv/bin/research-library run
```

Use this while the DAG is paused and no run is active to avoid competing
processing jobs.

## Project structure

```text
dags/paper_pipeline.py           Schedule, task dependencies, and retries
src/research_library/
|-- pipeline.py                 Processing stages and checkpoints
|-- pdf.py                      PDF conversion
|-- llm.py                      Local inference requests
|-- metadata.py                 Prompt, JSON schema, and validation
|-- storage.py                  SQLite operations
|-- render.py                   Static page generation
|-- notifications.py            Discord delivery
|-- drive.py                    Optional rclone download/upload
|-- config.py                   Environment settings and path handling
+-- templates/library.html      Page layout, styles, and browser filtering
scripts/                        Setup, startup, logging, and report utilities
tests/                          Automated checks
docs/                           Architecture, execution evidence, and report
```

## Limitations

- Filenames must be unique. Replacing the contents of an already processed file
  does not trigger reprocessing; use a new filename.
- Scanned PDFs require OCR, which is not configured. Corrupt files fail
  conversion and must be replaced with a valid copy.
- The full extracted text must fit within the configured model context. The
  input-size check uses an estimate; longer papers need a chunking strategy.
- JSON validation checks structure and basic types. Generated summaries still
  need to be checked against the original paper.
- The default configuration targets a single local machine with shared paths.

## Documentation

- [Architecture](docs/architecture.md)
- [Execution evidence](docs/execution-evidence.md)
- [Report draft](docs/report-draft.pdf)

The report source is `docs/report.html`. Regenerate the PDF with:

```bash
.venv/bin/python scripts/build_report.py
```

Export local run evidence with:

```bash
.venv/bin/python scripts/capture_evidence.py
```

## References

- [Apache Airflow quick start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- [Ollama](https://ollama.com/)
- [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM)
- [Rclone Google Drive configuration](https://rclone.org/drive/)
- [Discord webhooks](https://docs.discord.com/developers/resources/webhook#execute-webhook)
