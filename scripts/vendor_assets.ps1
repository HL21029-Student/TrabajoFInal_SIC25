#!/usr/bin/env pwsh
# Descarga assets de frontend (Vue, Quasar, Axios) para uso offline en web/vendor
# Uso: pwsh -File scripts/vendor_assets.ps1

$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Vendor = Join-Path $Root 'web' | Join-Path -ChildPath 'vendor'
if (!(Test-Path $Vendor)) { New-Item -ItemType Directory -Path $Vendor | Out-Null }

# Versiones (puedes fijarlas por variable de entorno o editar aquí)
$VUE_VER = if ($env:VUE_VER) { $env:VUE_VER } else { '3' }
$QUASAR_VER = if ($env:QUASAR_VER) { $env:QUASAR_VER } else { '2' }
$AXIOS_VER = if ($env:AXIOS_VER) { $env:AXIOS_VER } else { '1' }

function Download($url, $outFile) {
  Invoke-WebRequest -Uri $url -OutFile $outFile -UseBasicParsing
}

Write-Host "Descargando Vue @$VUE_VER ..."
Download "https://cdn.jsdelivr.net/npm/vue@$VUE_VER/dist/vue.global.prod.js" (Join-Path $Vendor 'vue.global.prod.js')

Write-Host "Descargando Quasar JS/CSS @$QUASAR_VER ..."
Download "https://cdn.jsdelivr.net/npm/quasar@$QUASAR_VER/dist/quasar.umd.prod.js" (Join-Path $Vendor 'quasar.umd.prod.js')
Download "https://cdn.jsdelivr.net/npm/quasar@$QUASAR_VER/dist/quasar.prod.css" (Join-Path $Vendor 'quasar.prod.css')

Write-Host "Descargando Axios @$AXIOS_VER ..."
Download "https://cdn.jsdelivr.net/npm/axios@$AXIOS_VER/dist/axios.min.js" (Join-Path $Vendor 'axios.min.js')

Write-Host "Listo. Archivos en $Vendor"
