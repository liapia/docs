#!/usr/bin/env bash
# Idempotent install for the design bot virtualenv.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "design-bot venv ready: $ROOT/.venv"
