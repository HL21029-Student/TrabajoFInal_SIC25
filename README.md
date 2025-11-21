# Sistema Contable — UI Quasar + Flask + pywebview

Interfaz moderna (Quasar) servida por Flask e integrada en una app de escritorio con pywebview. Soporta empaquetado en un binario único (onefile) con PyInstaller.

## Desarrollo rápido

Requisitos: Python 3.11. Usa entorno virtual para aislar dependencias.

```bash
# Crear venv (solo primera vez)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar assets frontend locales (una vez)
bash scripts/vendor_assets.sh

# Modo escritorio (pywebview + servidor)
python app_ui.py

# Modo navegador con auto-reload (más rápido para editar)
bash run_dev.sh
```

Abrir en el navegador: http://127.0.0.1:5000 (o puerto alterno si lo cambias).

### Ciclo de edición
1. Ejecuta `bash run_dev.sh` (auto-reload activo).
2. Edita archivos Python (`app_ui.py`, lógica en otros módulos) o `web/index.html`.
3. Guarda.
4. Flask recarga; refresca el navegador si cambiaste HTML/CSS.
5. Observa logs en la terminal para errores.

Si necesitas cambiar de puerto:
```bash
FLASK_RUN_PORT=5050 bash run_dev.sh
```

### Nota sobre pywebview
Si aparecen errores como `ModuleNotFoundError: gi` o `qtpy`:
- Sigue usando modo navegador (`run_dev.sh`).
- Opcional instalar soporte GTK/Qt:
	```bash
	sudo apt update && sudo apt install -y python3-gi gir1.2-webkit2-4.0
	sudo apt install -y python3-pyqt5
	pip install qtpy
	```

## Ejecutar en producción simple

```bash
source .venv/bin/activate
python app_ui.py
```

Esto inicia el servidor y, si es posible, abre la ventana nativa.

## Assets locales (offline)

Para funcionar sin Internet, el frontend usa copias locales de Vue/Quasar/Axios en `web/vendor/`.

- Linux/macOS:
	- `chmod +x scripts/vendor_assets.sh`
	- `./scripts/vendor_assets.sh`
- Windows (PowerShell):
	- `pwsh -File scripts/vendor_assets.ps1`

Variables opcionales para fijar versiones exactas antes de ejecutar (ejemplos):

```
export VUE_VER=3.5.24
export QUASAR_VER=2.18.5
export AXIOS_VER=1.6.8
```

Luego, `web/index.html` ya referencia estos archivos locales (`./vendor/*.js|.css`).

## Endpoints principales
- GET `/api/health`
- GET `/api/catalogo`
- GET `/api/diario`
- GET `/api/ventas`
- POST `/api/partida` { fecha, descripcion, cuenta_debe, cuenta_haber, monto }
- POST `/api/factura` { cliente, descripcion, monto }

## Empaquetar en ejecutable (Linux)

Instala PyInstaller en tu venv si no lo tienes:

```bash
/home/marvin/Documentos/SistemaContable/.venv/bin/pip install pyinstaller
```

Luego ejecuta el script de build:

```bash
chmod +x scripts/build_exe.sh
./scripts/build_exe.sh
```

El binario quedará en `dist/SistemaContable`.

Notas técnicas:
- `app_ui.py` ya detecta `sys._MEIPASS` usado por PyInstaller onefile, por lo que `web/` se sirve correctamente al estar empaquetado.
- Los assets del frontend usan Quasar y Vue via CDN; no se requiere build de frontend.
- Si requieres 100% offline, ejecuta primero el script de `vendor_assets` (ver arriba).

## Empaquetar en ejecutable (Windows)

Debes compilar en Windows para obtener `.exe`.

1) Instala dependencias en un venv (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
```

2) (Opcional) Descargar assets locales:

```
pwsh -File scripts/vendor_assets.ps1
```

3) Construir con PyInstaller (usa `;` en --add-data):

```
pwsh -File scripts/build_exe.ps1
```

El ejecutable quedará en `dist/SistemaContable.exe`.

## Troubleshooting
- Si no se abre la ventana de escritorio, el servidor queda disponible en http://127.0.0.1:5000.
- En entornos sin aceleración gráfica o sin X/Wayland, pywebview puede fallar; usa el navegador.
- Si `web/` no aparece en el ejecutable, verifica la opción `--add-data "web:web"` en el script de build.
- En Windows, recuerda que el separador en `--add-data` es `;` (ej: `--add-data "web;web"`).
- Si tienes rutas o módulos nuevos, PyInstaller los incluirá automáticamente; para casos especiales, agrega `hiddenimports` en una spec.
