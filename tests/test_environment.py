import json
import os
from pathlib import Path
import subprocess
import sys
import shutil

import pytest

from dotenv import dotenv_values

from research_library.config import load_settings, resolve_project_path
from research_library.llm import extract_metadata

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(not shutil.which("wslpath"), reason="Requires Windows path conversion in WSL")
@pytest.mark.parametrize("value", [r"C:\Users\Professor\My Drive\ResearchLibrary\papers", "C:/Users/Professor/My Drive/ResearchLibrary/papers"])
def test_windows_drive_paths_are_translated(value, tmp_path):
    assert resolve_project_path(value, tmp_path) == Path("/mnt/c/Users/Professor/My Drive/ResearchLibrary/papers")


def test_windows_path_fails_clearly_outside_wsl(monkeypatch, tmp_path):
    monkeypatch.setattr("research_library.config.shutil.which", lambda name: None)
    with pytest.raises(ValueError, match="require WSL"):
        resolve_project_path("C:/Users/Professor/papers", tmp_path)


def test_startup_loader_quotes_webhooks_and_resolves_relative_paths(tmp_path):
    root = tmp_path / "demo project"
    (root / "scripts").mkdir(parents=True)
    (root / ".venv").symlink_to(Path(sys.executable).parent.parent, target_is_directory=True)
    helper = root / "scripts/load_env.sh"
    helper.write_text((ROOT / "scripts/load_env.sh").read_text())
    marker = tmp_path / "must-not-exist"
    webhook = f"https://example.invalid/hook?thread_id=123&value=$(touch {marker})"
    (root / ".env").write_text(
        "OLLAMA_MODELS='./weights folder'\n"
        "AIRFLOW_HOME='./runtime'\n"
        "LLM_THREADS=4\n"
        f"DISCORD_WEBHOOK_URL='{webhook}'\n"
    )
    environment = os.environ.copy()
    for key in ("OLLAMA_MODELS", "AIRFLOW_HOME", "DISCORD_WEBHOOK_URL"):
        environment.pop(key, None)
    environment["LLM_THREADS"] = "6"  # Explicit shell settings take precedence.
    command = 'source "$1" && "$2" -B -c \'import json,os; print(json.dumps({key:os.environ[key] for key in ["OLLAMA_MODELS","AIRFLOW_HOME","LLM_THREADS","DISCORD_WEBHOOK_URL"]}))\''
    result = subprocess.run(["bash", "-c", command, "test", str(helper), sys.executable],
                            env=environment, cwd=tmp_path, capture_output=True, text=True, check=True)
    values = json.loads(result.stdout)
    assert values["OLLAMA_MODELS"] == str(root / "weights folder")
    assert values["AIRFLOW_HOME"] == str(root / "runtime")
    assert values["LLM_THREADS"] == "6"
    assert values["DISCORD_WEBHOOK_URL"] == webhook
    assert not marker.exists()


def test_application_reads_model_tuning_and_literal_webhook(tmp_path, monkeypatch):
    for key in dotenv_values(ROOT / ".env.example"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("RESEARCH_LIBRARY_ROOT", str(tmp_path))
    (tmp_path / ".env").write_text(
        "LLM_THREADS=3\nLLM_CONTEXT=8192\nLLM_MAX_OUTPUT_TOKENS=256\n"
        "LLM_TEMPERATURE=0.2\nLLM_SEED=7\nLLM_KEEP_ALIVE=2m\nLLM_NUM_GPU=0\n"
        "DISCORD_ENABLED=true\nDISCORD_WEBHOOK_URL='https://example.invalid/${literal}'\n"
    )
    settings = load_settings()
    assert (settings.threads, settings.context, settings.max_output) == (3, 8192, 256)
    assert (settings.temperature, settings.seed, settings.keep_alive, settings.num_gpu) == (0.2, 7, "2m", 0)
    assert settings.webhook_url == "https://example.invalid/${literal}"
    assert settings.discord_enabled


def test_model_tuning_is_sent_to_ollama(monkeypatch):
    metadata = {"title": "Paper", "summary": "Summary", "keywords": ["systems"], "category": "Computing"}
    requests = []

    def fake_request(base_url, endpoint, payload, timeout):
        requests.append(payload)
        return {"message": {"content": json.dumps(metadata)}}

    monkeypatch.setattr("research_library.llm.request_json", fake_request)
    result, _ = extract_metadata("Paper text", base_url="http://localhost", model="test", context=8192,
                                 threads=3, max_output=256, temperature=0.2, seed=7, keep_alive="2m", num_gpu=0)
    assert result == metadata
    assert requests[0]["options"] == {"num_gpu": 0, "num_ctx": 8192, "num_thread": 3,
                                       "num_predict": 256, "temperature": 0.2, "seed": 7}
    assert requests[0]["keep_alive"] == "2m"
