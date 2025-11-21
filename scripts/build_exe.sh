#!/usr/bin/env bash
set -euo pipefail
# Build onefile executable, bundling the web assets
# Usage: ./scripts/build_exe.sh

VENV_PY="${VENV_PY:-/home/marvin/Documentos/SistemaContable/.venv/bin/python}"
PYI="${PYI:-$VENV_PY -m PyInstaller}"

cd "$(dirname "$0")/.."

$PYI \
  --name "SistemaContable" \
  --onefile \
  --add-data "web:web" \
  app_ui.py

echo "\nBuild listo. Ejecutable: dist/SistemaContable"
