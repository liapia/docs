#!/usr/bin/env bash
# Idempotent install for the design bot virtualenv.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  echo "ensurepip missing — installing python3-venv..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-venv python3.12-venv
fi

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "design-bot venv ready: $ROOT/.venv"
