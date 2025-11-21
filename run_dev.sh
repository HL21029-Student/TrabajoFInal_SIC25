#!/usr/bin/env bash
set -euo pipefail

# Script de desarrollo rápido para ver cambios al instante.
# Uso:
#   bash run_dev.sh
# Requisitos: entorno virtual creado e instalaciones hechas (requirements.txt)

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

if [ ! -d .venv ]; then
  echo "[run_dev] No existe .venv. Creando..."
  python3 -m venv .venv
fi

source .venv/bin/activate

# Instalar dependencias si falta Flask
python -c "import flask" 2>/dev/null || pip install -r requirements.txt

export FLASK_APP=app_ui.py
export FLASK_ENV=development
export FLASK_RUN_PORT=${FLASK_RUN_PORT:-5000}

# Si el puerto está ocupado, avisar y sugerir otro
if command -v lsof >/dev/null 2>&1; then
  if lsof -i :"$FLASK_RUN_PORT" >/dev/null 2>&1; then
    echo "[run_dev] Puerto $FLASK_RUN_PORT en uso. Cambia FLASK_RUN_PORT o libera el puerto."
    echo "Ejemplo: FLASK_RUN_PORT=5050 bash run_dev.sh"
  fi
fi

echo "[run_dev] Iniciando servidor Flask con auto-reload en puerto $FLASK_RUN_PORT"
# Usamos flask run para que active el reloader; pywebview se omite para velocidad
flask run --reload --debug --host 127.0.0.1 --port "$FLASK_RUN_PORT"
