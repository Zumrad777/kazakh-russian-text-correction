#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found. Install Python 3.10+ from https://www.python.org/downloads/"
  exit 1
fi
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ""
echo "Starting TilTüzету at http://127.0.0.1:8000"
echo "API docs: http://127.0.0.1:8000/docs"
exec uvicorn app:app --reload
