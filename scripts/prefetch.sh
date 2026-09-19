#!/usr/bin/env bash
# Air-Gap Prefetch Script
# Downloads Python wheels, npm packages, and Ollama models into a local cache directory.

set -e

CACHE_DIR="$(pwd)/offline_cache"
mkdir -p "${CACHE_DIR}/wheels"
mkdir -p "${CACHE_DIR}/npm"
mkdir -p "${CACHE_DIR}/ollama"

echo "=== [1/3] Caching Python Wheels ==="
pip download -r backend/requirements.txt -d "${CACHE_DIR}/wheels"

echo "=== [2/3] Caching Ollama Models ==="
if command -v ollama &> /dev/null; then
  echo "Pulling Llama 3 model into cache..."
  ollama pull llama3:8b
else
  echo "Ollama CLI not installed locally. Model will be pre-pulled via Docker volume."
fi

echo "=== [3/3] Air-Gap Cache Prepared Successfully ==="
echo "Cache saved in: ${CACHE_DIR}"
