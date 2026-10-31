# Execution screenshots

These screenshots document the evaluated Drive-to-Discord run. They are included
without changing the captured interface or results.

| File | Contents |
| --- | --- |
| `01-airflow-success.png` | Successful processing run and task states |
| `02-airflow-runs.png` | Run history, including empty follow-up scans |
| `03-discord.png` | DAG-bot paper notifications |
| `04-library.png` | Generated searchable library |
| `05-drive-output.png` | Uploaded index.html in Google Drive |

Airflow dashboard timestamps use UTC+02:00. The logical run identifier uses UTC.
A skipped failure watcher is expected on a successful run. The report uses the
processing run rather than treating an empty scan as evidence of inference.
