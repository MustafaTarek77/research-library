# Local execution evidence

Captured at 2026-10-29T17:49:48.402054+00:00.

These are actual Airflow standalone runs, not the sequential diagnostic runner.
The configured library is a local demo folder. Drive sync is not configured;
Discord delivery is disabled pending user configuration.

## DAG runs

| Run ID | State | Duration |
| --- | --- | ---: |
| `scheduled__2026-10-29T17:40:00+00:00` | success | 155.04s |
| `scheduled__2026-10-29T17:45:00+00:00` | success | 4.37s |
| `verification_bad_pdf_20261029` | failed | 36.16s |
| `verification_recovery_20261029` | success | 1.62s |

## Task execution

| Run | Task | Map index | State | Attempt |
| --- | --- | ---: | --- | ---: |
| `scheduled__2026-10-29T17:40:00+00:00` | `convert_pdf` | 0 | success | 1 |
| `scheduled__2026-10-29T17:40:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T17:40:00+00:00` | `extract_metadata` | 0 | success | 1 |
| `scheduled__2026-10-29T17:40:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T17:40:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T17:40:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:40:00+00:00` | `save_metadata` | 0 | success | 1 |
| `scheduled__2026-10-29T17:45:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:45:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T17:45:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:45:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T17:45:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T17:45:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:45:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `verification_bad_pdf_20261029` | `convert_pdf` | 0 | failed | 2 |
| `verification_bad_pdf_20261029` | `discover_pdfs` | -1 | success | 1 |
| `verification_bad_pdf_20261029` | `extract_metadata` | -1 | upstream_failed | 0 |
| `verification_bad_pdf_20261029` | `notify_discord` | -1 | success | 1 |
| `verification_bad_pdf_20261029` | `regenerate_html` | -1 | success | 1 |
| `verification_bad_pdf_20261029` | `report_failure` | -1 | failed | 1 |
| `verification_bad_pdf_20261029` | `save_metadata` | -1 | upstream_failed | 0 |
| `verification_recovery_20261029` | `convert_pdf` | -1 | skipped | 0 |
| `verification_recovery_20261029` | `discover_pdfs` | -1 | success | 1 |
| `verification_recovery_20261029` | `extract_metadata` | -1 | skipped | 0 |
| `verification_recovery_20261029` | `notify_discord` | -1 | success | 1 |
| `verification_recovery_20261029` | `regenerate_html` | -1 | success | 1 |
| `verification_recovery_20261029` | `report_failure` | -1 | skipped | 0 |
| `verification_recovery_20261029` | `save_metadata` | -1 | skipped | 0 |

The deliberately invalid PDF fixture was removed after verifying failed conversion,
successful HTML publication, and overall DAG failure through the watcher.
A skipped failure watcher is expected on successful runs.

## Application state

- Stored papers: 1.
- Pending notifications: 1.
- Generated page exists: True.
- The initial paper was the complete 13-page MapReduce PDF.
- A later scheduled scan found no new PDFs and avoided another LLM call.
- LLM progress heartbeats were recorded every 15 seconds in Airflow task logs.

## Checks

The automated suite covers basic JSON validation and one retry, source-change detection,
filename deduplication, metadata checkpoint reuse, HTML escaping and PDF URL encoding,
notification checkpoint recovery, disabled delivery, and webhook error redaction.
The generated page's JavaScript was syntax-checked with Node. Interactive filtering
should also be reviewed in the user's browser before the final demonstration.

## Remaining submission work

Configure and verify Google Drive sync and real Discord delivery. Add group members
and the GitHub repository URL, update the report, and generate its final PDF.
