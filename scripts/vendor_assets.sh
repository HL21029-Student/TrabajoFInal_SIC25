#!/usr/bin/env bash
# Descarga assets de frontend (Vue, Quasar, Axios) para uso offline en web/vendor
# Uso: ./scripts/vendor_assets.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/web/vendor"
mkdir -p "$VENDOR_DIR"

# Versiones (puedes fijarlas por variable de entorno o editar aquí)
: "${VUE_VER:=3}"
: "${QUASAR_VER:=2}"
: "${AXIOS_VER:=1}"

# Si quieres fijar parches exactos, por ejemplo:
# export VUE_VER=3.5.24
# export QUASAR_VER=2.18.5
# export AXIOS_VER=1.6.8

echo "Descargando Vue @${VUE_VER} ..."
curl -fL "https://cdn.jsdelivr.net/npm/vue@${VUE_VER}/dist/vue.global.prod.js" -o "$VENDOR_DIR/vue.global.prod.js"

echo "Descargando Quasar JS/CSS @${QUASAR_VER} ..."
curl -fL "https://cdn.jsdelivr.net/npm/quasar@${QUASAR_VER}/dist/quasar.umd.prod.js" -o "$VENDOR_DIR/quasar.umd.prod.js"
curl -fL "https://cdn.jsdelivr.net/npm/quasar@${QUASAR_VER}/dist/quasar.prod.css" -o "$VENDOR_DIR/quasar.prod.css"

echo "Descargando Axios @${AXIOS_VER} ..."
curl -fL "https://cdn.jsdelivr.net/npm/axios@${AXIOS_VER}/dist/axios.min.js" -o "$VENDOR_DIR/axios.min.js"

# Opcional: extras de iconos locales (material-icons) y fuentes podría añadirse aquí
# Nota: actualmente se usan desde CDN; si necesitas 100% offline, agrega descargas y ajusta index.html

echo "Listo. Archivos en $VENDOR_DIR"
