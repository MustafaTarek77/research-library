#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/load_env.sh"
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11435}"
export OLLAMA_MODELS="${OLLAMA_MODELS:-$project_root/.cache/ollama}"
export OLLAMA_NUM_PARALLEL="${OLLAMA_NUM_PARALLEL:-1}"
export OLLAMA_MAX_LOADED_MODELS="${OLLAMA_MAX_LOADED_MODELS:-1}"
export OLLAMA_CONTEXT_LENGTH="${OLLAMA_CONTEXT_LENGTH:-32768}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:--1}"
export ROCR_VISIBLE_DEVICES="${ROCR_VISIBLE_DEVICES:--1}"
export OLLAMA_VULKAN="${OLLAMA_VULKAN:-false}"
export OLLAMA_NO_CLOUD="${OLLAMA_NO_CLOUD:-true}"
exec ollama serve
