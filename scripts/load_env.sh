#!/usr/bin/env bash
# Source this helper. dotenv values are shell-quoted, never executed as code.
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
project_python="$project_root/.venv/bin/python"
if [[ ! -x "$project_python" ]]; then
  project_python="$project_root/.airflow-venv/bin/python"
fi
project_env_exports="$("$project_python" -B - "$project_root" <<'PY'
import os
from pathlib import Path
import re
import shlex
import sys
from dotenv import dotenv_values
from research_library.config import resolve_project_path

root = Path(sys.argv[1])
path_keys = {
    'PAPERS_DIR', 'OUTPUT_DIR', 'DATABASE_PATH', 'WORK_DIR', 'LOG_FILE',
    'AIRFLOW_HOME', 'AIRFLOW__CORE__DAGS_FOLDER', 'OLLAMA_MODELS', 'RCLONE_CONFIG',
}
for key, configured in dotenv_values(root / '.env', interpolate=False).items():
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
        raise SystemExit('Invalid environment variable name in .env')
    value = os.environ.get(key, configured)
    if value is None:
        continue
    if key in path_keys and value:
        value = str(resolve_project_path(value, root))
    print('export ' + key + '=' + shlex.quote(value))
PY
)" || return 1
eval "$project_env_exports"
unset project_env_exports project_python
