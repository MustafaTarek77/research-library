"""Scheduled local research library. Task bodies import application code lazily."""

from datetime import datetime, timedelta, timezone
import os

from airflow.sdk import DAG, task
from airflow.exceptions import AirflowException


with DAG(
    dag_id="paper_pipeline",
    description="PDF → Markdown → local LLM → SQLite → HTML → Discord",
    schedule=os.getenv("PIPELINE_SCHEDULE", "*/5 * * * *"),
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    max_active_runs=int(os.getenv("PIPELINE_MAX_ACTIVE_RUNS", "1")),
    max_active_tasks=int(os.getenv("PIPELINE_MAX_ACTIVE_TASKS", "1")),
    is_paused_upon_creation=True,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=int(os.getenv("PIPELINE_RETRY_DELAY_SECONDS", "30")))},
    tags=["assignment-3", "local-llm"],
) as dag:

    @task
    def download_drive_pdfs():
        from research_library.config import load_settings
        from research_library.drive import download_papers
        return download_papers(load_settings())

    @task
    def discover_pdfs():
        from research_library.config import load_settings
        from research_library.pipeline import discover
        return discover(load_settings())

    @task
    def convert_pdf(paper):
        from research_library.config import load_settings
        from research_library.pipeline import convert
        return convert(paper, load_settings())

    # Invalid JSON already gets exactly one retry inside the LLM client.
    @task(retries=0, execution_timeout=timedelta(minutes=int(os.getenv("PIPELINE_EXTRACTION_TIMEOUT_MINUTES", "35"))))
    def extract_metadata(paper):
        from research_library.config import load_settings
        from research_library.pipeline import generate_metadata
        return generate_metadata(paper, load_settings())

    @task
    def save_metadata(paper):
        from research_library.config import load_settings
        from research_library.pipeline import persist
        return persist(paper, load_settings())

    @task(trigger_rule="all_done")
    def regenerate_html():
        from research_library.config import load_settings
        from research_library.render import render_library
        return render_library(load_settings())

    @task
    def upload_drive_html():
        from research_library.config import load_settings
        from research_library.drive import upload_html
        return upload_html(load_settings())

    @task
    def notify_discord():
        from research_library.config import load_settings
        from research_library.notifications import notify_pending
        return notify_pending(load_settings())

    @task(trigger_rule="one_failed", retries=0)
    def report_failure():
        raise AirflowException("A pipeline task failed. Inspect the failed task's logs.")

    downloaded = download_drive_pdfs()
    discovered = discover_pdfs()
    downloaded >> discovered
    converted = convert_pdf.expand(paper=discovered)
    extracted = extract_metadata.expand(paper=converted)
    stored = save_metadata.expand(paper=extracted)
    published = regenerate_html()
    uploaded = upload_drive_html()
    stored >> published >> uploaded >> notify_discord()
    # all_done publication must not bypass an unsuccessful input transfer.
    downloaded >> uploaded
    # Publishing successful records must not hide an earlier processing failure.
    watched_tasks = list(dag.tasks)
    watched_tasks >> report_failure()
