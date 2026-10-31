# Local execution evidence

Captured at 2026-10-31T14:10:37.002621+00:00.

These are actual Airflow standalone runs, not the sequential diagnostic runner.
Rclone transfers enabled: True.
Discord delivery enabled: True.

## DAG runs

| Run ID | State | Duration |
| --- | --- | ---: |
| `scheduled__2026-10-29T17:40:00+00:00` | success | 155.04s |
| `scheduled__2026-10-29T17:45:00+00:00` | success | 4.37s |
| `verification_bad_pdf_20261029` | failed | 36.16s |
| `verification_recovery_20261029` | success | 1.62s |
| `scheduled__2026-10-29T17:50:00+00:00` | success | 2.98s |
| `scheduled__2026-10-29T17:55:00+00:00` | success | 1.91s |
| `scheduled__2026-10-29T18:00:00+00:00` | success | 2.92s |
| `scheduled__2026-10-29T18:05:00+00:00` | success | 2.90s |
| `scheduled__2026-10-29T18:10:00+00:00` | success | 3.94s |
| `scheduled__2026-10-29T18:15:00+00:00` | success | 3.12s |
| `scheduled__2026-10-29T18:20:00+00:00` | success | 3.93s |
| `scheduled__2026-10-29T18:25:00+00:00` | success | 3.91s |
| `scheduled__2026-10-29T18:30:00+00:00` | success | 3.80s |
| `scheduled__2026-10-29T18:35:00+00:00` | success | 3.44s |
| `scheduled__2026-10-29T18:40:00+00:00` | success | 3.63s |
| `scheduled__2026-10-29T18:45:00+00:00` | success | 4.03s |
| `scheduled__2026-10-29T18:50:00+00:00` | success | 4.45s |
| `scheduled__2026-10-29T18:55:00+00:00` | success | 4.36s |
| `scheduled__2026-10-29T19:00:00+00:00` | success | 3.39s |
| `scheduled__2026-10-29T19:05:00+00:00` | success | 3.03s |
| `scheduled__2026-10-29T19:10:00+00:00` | success | 3.80s |
| `scheduled__2026-10-29T19:15:00+00:00` | success | 11985.44s |
| `scheduled__2026-10-29T22:55:00+00:00` | success | 5.97s |
| `scheduled__2026-10-29T23:00:00+00:00` | success | 12.01s |
| `scheduled__2026-10-30T18:20:00+00:00` | success | 5.04s |
| `scheduled__2026-10-30T18:25:00+00:00` | success | 5.42s |
| `scheduled__2026-10-30T18:30:00+00:00` | success | 4.88s |
| `scheduled__2026-10-30T18:35:00+00:00` | success | 4.40s |
| `manual__2026-10-30T18:35:00.127826+00:00` | success | 4.76s |
| `manual__2026-10-30T18:39:06.795224+00:00` | failed | 36.01s |
| `scheduled__2026-10-30T18:40:00+00:00` | failed | 34.78s |
| `scheduled__2026-10-30T18:45:00+00:00` | failed | 36.29s |
| `scheduled__2026-10-30T18:50:00+00:00` | failed | 43.93s |
| `manual__2026-10-30T18:50:48.118762+00:00` | success | 153.13s |
| `scheduled__2026-10-30T18:55:00+00:00` | success | 2.80s |
| `scheduled__2026-10-30T19:00:00+00:00` | success | 4.18s |
| `scheduled__2026-10-30T19:05:00+00:00` | success | 5.20s |
| `scheduled__2026-10-30T19:10:00+00:00` | success | 4.92s |
| `scheduled__2026-10-31T13:35:00+00:00` | success | 673.06s |
| `scheduled__2026-10-31T13:45:00+00:00` | success | 9.93s |
| `scheduled__2026-10-31T13:50:00+00:00` | success | 12.13s |
| `scheduled__2026-10-31T13:55:00+00:00` | success | 12.10s |
| `scheduled__2026-10-31T14:00:00+00:00` | success | 12.53s |
| `scheduled__2026-10-31T14:05:00+00:00` | success | 12.73s |
| `scheduled__2026-10-31T14:10:00+00:00` | success | 13.16s |

## Task execution

| Run | Task | Map index | State | Attempt |
| --- | --- | ---: | --- | ---: |
| `manual__2026-10-30T18:35:00.127826+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `discover_pdfs` | -1 | success | 1 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `notify_discord` | -1 | success | 1 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `regenerate_html` | -1 | success | 1 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `report_failure` | -1 | skipped | 0 |
| `manual__2026-10-30T18:35:00.127826+00:00` | `save_metadata` | -1 | skipped | 0 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `convert_pdf` | 0 | failed | 2 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `discover_pdfs` | -1 | success | 1 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `extract_metadata` | -1 | upstream_failed | 0 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `notify_discord` | -1 | success | 1 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `regenerate_html` | -1 | success | 1 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `report_failure` | -1 | failed | 1 |
| `manual__2026-10-30T18:39:06.795224+00:00` | `save_metadata` | -1 | upstream_failed | 0 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `convert_pdf` | 0 | success | 1 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `discover_pdfs` | -1 | success | 1 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `extract_metadata` | 0 | success | 1 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `notify_discord` | -1 | success | 1 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `regenerate_html` | -1 | success | 1 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `report_failure` | -1 | skipped | 0 |
| `manual__2026-10-30T18:50:48.118762+00:00` | `save_metadata` | 0 | success | 1 |
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
| `scheduled__2026-10-29T17:50:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:50:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T17:50:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:50:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T17:50:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T17:50:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:50:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:55:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:55:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T17:55:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:55:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T17:55:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T17:55:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T17:55:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:00:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:00:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:00:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:00:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:00:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:00:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:00:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:05:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:05:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:05:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:05:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:05:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:05:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:05:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:10:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:10:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:10:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:10:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:10:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:10:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:10:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:15:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:15:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:15:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:15:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:15:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:15:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:15:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:20:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:20:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:20:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:20:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:20:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:20:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:20:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:25:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:25:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:25:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:25:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:25:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:25:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:25:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:30:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:30:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:30:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:30:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:30:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:30:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:30:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:35:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:35:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:35:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:35:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:35:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:35:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:35:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:40:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:40:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:40:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:40:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:40:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:40:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:40:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:45:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:45:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:45:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:45:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:45:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:45:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:45:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:50:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:50:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:50:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:50:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:50:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:50:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:50:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:55:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:55:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T18:55:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:55:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T18:55:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T18:55:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T18:55:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:00:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:00:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T19:00:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:00:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T19:00:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T19:00:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:00:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:05:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:05:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T19:05:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:05:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T19:05:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T19:05:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:05:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:10:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:10:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T19:10:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:10:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T19:10:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T19:10:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:10:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:15:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:15:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T19:15:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:15:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T19:15:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T19:15:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T19:15:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T22:55:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T22:55:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T22:55:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T22:55:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T22:55:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T22:55:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T22:55:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T23:00:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-29T23:00:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-29T23:00:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-29T23:00:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-29T23:00:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-29T23:00:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-29T23:00:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:20:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:20:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:20:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:20:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:20:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:20:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:20:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:25:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:25:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:25:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:25:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:25:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:25:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:25:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:30:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:30:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:30:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:30:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:30:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:30:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:30:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:35:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:35:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:35:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:35:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:35:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:35:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:35:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:40:00+00:00` | `convert_pdf` | 0 | failed | 2 |
| `scheduled__2026-10-30T18:40:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:40:00+00:00` | `extract_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:40:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:40:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:40:00+00:00` | `report_failure` | -1 | failed | 1 |
| `scheduled__2026-10-30T18:40:00+00:00` | `save_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:45:00+00:00` | `convert_pdf` | 0 | failed | 2 |
| `scheduled__2026-10-30T18:45:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:45:00+00:00` | `extract_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:45:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:45:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:45:00+00:00` | `report_failure` | -1 | failed | 1 |
| `scheduled__2026-10-30T18:45:00+00:00` | `save_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:50:00+00:00` | `convert_pdf` | 0 | failed | 2 |
| `scheduled__2026-10-30T18:50:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:50:00+00:00` | `extract_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:50:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:50:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:50:00+00:00` | `report_failure` | -1 | failed | 1 |
| `scheduled__2026-10-30T18:50:00+00:00` | `save_metadata` | -1 | upstream_failed | 0 |
| `scheduled__2026-10-30T18:55:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:55:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T18:55:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:55:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T18:55:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T18:55:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T18:55:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:00:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:00:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T19:00:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:00:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T19:00:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T19:00:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:00:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:05:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:05:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T19:05:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:05:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T19:05:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T19:05:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:05:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:10:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:10:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-30T19:10:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:10:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-30T19:10:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-30T19:10:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-30T19:10:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:35:00+00:00` | `convert_pdf` | 0 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `convert_pdf` | 1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `extract_metadata` | 0 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `extract_metadata` | 1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:35:00+00:00` | `save_metadata` | 0 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `save_metadata` | 1 | success | 1 |
| `scheduled__2026-10-31T13:35:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:45:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:45:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:45:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:45:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:45:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T13:45:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:45:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:45:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:45:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:50:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:50:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:50:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:50:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:50:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T13:50:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:50:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:50:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:50:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:55:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:55:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:55:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T13:55:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:55:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T13:55:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T13:55:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:55:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T13:55:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:00:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:00:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:00:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:00:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:00:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T14:00:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:00:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:00:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:00:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:05:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:05:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:05:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:05:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:05:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T14:05:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:05:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:05:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:05:00+00:00` | `upload_drive_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:10:00+00:00` | `convert_pdf` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:10:00+00:00` | `discover_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:10:00+00:00` | `download_drive_pdfs` | -1 | success | 1 |
| `scheduled__2026-10-31T14:10:00+00:00` | `extract_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:10:00+00:00` | `notify_discord` | -1 | success | 1 |
| `scheduled__2026-10-31T14:10:00+00:00` | `regenerate_html` | -1 | success | 1 |
| `scheduled__2026-10-31T14:10:00+00:00` | `report_failure` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:10:00+00:00` | `save_metadata` | -1 | skipped | 0 |
| `scheduled__2026-10-31T14:10:00+00:00` | `upload_drive_html` | -1 | success | 1 |
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

- Stored papers: 4.
- Pending notifications: 0.
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

## Reproduction

The README documents setup and execution. The final technical report is available in
docs/technical-report.pdf, with its editable source in docs/report.md and screenshots
in screenshots/. Run this script after another experiment to refresh the state tables.
