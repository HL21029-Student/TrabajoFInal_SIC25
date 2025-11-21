#!/usr/bin/env pwsh
# Construye ejecutable onefile en Windows con PyInstaller
# Uso: pwsh -File scripts/build_exe.ps1

$ErrorActionPreference = 'Stop'

# Ruta opcional a Python/venv
$env:VENV_PY = if ($env:VENV_PY) { $env:VENV_PY } else { '' }

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

# Resuelve comando de PyInstaller
if ($env:VENV_PY -and (Test-Path $env:VENV_PY)) {
  $PYI = "$env:VENV_PY -m PyInstaller"
} else {
  $PYI = "pyinstaller"
}

# Nota: En Windows, --add-data usa ';' como separador PATH;DEST
$cmd = @(
  $PYI,
  '--name', 'SistemaContable',
  '--onefile',
  '--add-data', 'web;web',
  'app_ui.py'
) -join ' '

Write-Host "Ejecutando: $cmd"
Invoke-Expression $cmd

Write-Host "`nBuild listo. Ejecutable: dist/SistemaContable.exe"
