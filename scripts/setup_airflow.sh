#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
python3 -m venv .airflow-venv
.airflow-venv/bin/python -m pip install 'apache-airflow==3.3.2' \
  --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt
.airflow-venv/bin/python -m pip install -e .
echo 'Installed. Start Ollama with bash scripts/serve_cpu.sh and Airflow with bash scripts/start_airflow.sh.'
