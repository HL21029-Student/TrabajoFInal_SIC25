#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UI de escritorio con Flask + Quasar (CDN) + pywebview

Este módulo levanta un servidor Flask que sirve la carpeta `web/` y expone
APIs para interactuar con la base de datos y operaciones contables ya
implementadas en los módulos existentes. Luego, abre una ventana nativa con
pywebview apuntando a http://127.0.0.1:5000.

Para empaquetar en un ejecutable (Linux):
  - pip install -r requirements.txt
  - pyinstaller --name "SistemaContable" --onefile --add-data "web:web" app_ui.py

Nota empaquetado: dentro de un binario onefile, los assets se extraen a un
directorio temporal accesible vía `sys._MEIPASS`. Este archivo ya gestiona
esa ruta al configurar Flask.
"""

import os
import sys
import threading
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, request, send_from_directory

# Reutilizamos la lógica existente desde sistema_completo
try:
    # Import directo si está en el mismo directorio
    import sistema_completo as sc
except Exception:
    # Como fallback, intentar importar por nombre absoluto
    from . import sistema_completo as sc  # type: ignore


def _base_path() -> str:
    """Devuelve la ruta base donde viven los assets `web/`.

    - Cuando se ejecuta normal: usa el directorio del archivo actual.
    - Cuando se ejecuta empaquetado con PyInstaller (onefile): usa sys._MEIPASS.
    """
    if hasattr(sys, "_MEIPASS"):
        return getattr(sys, "_MEIPASS")  # type: ignore[attr-defined]
    return os.path.abspath(os.path.dirname(__file__))


def create_app() -> Flask:
    base = _base_path()
    web_dir = os.path.join(base, "web")

    app = Flask(
        __name__,
        static_folder=web_dir,
        static_url_path="",  # sirve /web/* en la raíz
    )

    # ========= Rutas frontend =========
    @app.get("/")
    def index():
        # Sirve el index.html de la SPA
        return send_from_directory(web_dir, "index.html")

    # ========= APIs =========
    @app.get("/api/health")
    def health():
        return {"status": "ok", "time": datetime.now().isoformat()}

    @app.get("/api/catalogo")
    def api_catalogo():
        cat = sc.CatalogoCuentas()
        cuentas = cat.mostrar_catalogo()  # devuelve lista de tuplas
        data = [
            {"codigo": c[0], "nombre": c[1], "tipo": c[2], "nivel": c[3]}
            for c in cuentas
        ]
        return jsonify(data)

    @app.get("/api/diario")
    def api_diario():
        diario = sc.LibroDiario()
        partidas = diario.mostrar_diario()  # lista de filas
        data = [
            {
                "id": p[0],
                "fecha": p[1],
                "descripcion": p[2],
                "cuenta_debe": p[3],
                "cuenta_haber": p[4],
                "monto": p[5],
                "tipo": p[6],
            }
            for p in partidas
        ]
        return jsonify(data)

    @app.get("/api/mayor")
    def api_mayor():
        """Libro Mayor: saldos debe/haber por cuenta"""
        mayor = sc.Mayorizacion()
        saldos = mayor.calcular_saldos_cuentas()
        data = [
            {
                "cuenta": cuenta,
                "debe": mov["debe"],
                "haber": mov["haber"],
                "saldo": mov["debe"] - mov["haber"],
            }
            for cuenta, mov in saldos.items()
        ]
        return jsonify(data)

    @app.get("/api/balanza")
    def api_balanza():
        """Balanza de Comprobación con totales"""
        mayor = sc.Mayorizacion()
        saldos = mayor.calcular_saldos_cuentas()
        total_debe = sum(m["debe"] for m in saldos.values())
        total_haber = sum(m["haber"] for m in saldos.values())
        data = {
            "cuentas": [
                {
                    "cuenta": cuenta,
                    "debe": mov["debe"],
                    "haber": mov["haber"],
                    "saldo": mov["debe"] - mov["haber"],
                }
                for cuenta, mov in saldos.items()
            ],
            "totales": {
                "debe": total_debe,
                "haber": total_haber,
                "diferencia": total_debe - total_haber,
            },
        }
        return jsonify(data)

    @app.get("/api/balance-general")
    def api_balance_general():
        """Balance General: activos, pasivos, capital"""
        estados = sc.EstadosFinancieros()
        # Reutilizar lógica de balance_general pero devolver JSON
        mayor = sc.Mayorizacion()
        saldos = mayor.calcular_saldos_cuentas()
        
        activos = 0
        pasivos = 0
        capital = 0
        ingresos = 0
        gastos = 0
        
        catalogo = sc.CatalogoCuentas()
        db = catalogo.db
        
        for cuenta in saldos.keys():
            tipo_info = db.obtener_datos(
                "SELECT tipo FROM catalogo_cuentas WHERE codigo = ?", (cuenta,)
            )
            if tipo_info:
                tipo = tipo_info[0][0]
                saldo_cuenta = saldos[cuenta]["debe"] - saldos[cuenta]["haber"]
                
                if tipo == "Activo":
                    activos += saldo_cuenta
                elif tipo == "Pasivo":
                    pasivos += saldo_cuenta
                elif tipo == "Capital":
                    capital += saldo_cuenta
                elif tipo == "Ingreso":
                    ingresos += saldo_cuenta
                elif tipo == "Gasto":
                    gastos += saldo_cuenta
        
        utilidad = ingresos - gastos
        
        return jsonify({
            "activos": activos,
            "pasivos": pasivos,
            "capital": capital,
            "ingresos": ingresos,
            "gastos": gastos,
            "utilidad": utilidad,
            "ecuacion": activos == (pasivos + capital + utilidad)
        })
        data = [
            {
                "id": p[0],
                "fecha": p[1],
                "descripcion": p[2],
                "cuenta_debe": p[3],
                "cuenta_haber": p[4],
                "monto": p[5],
                "tipo": p[6],
            }
            for p in partidas
        ]
        return jsonify(data)

    @app.post("/api/partida")
    def api_registrar_partida():
        data = request.get_json()
        diario = sc.LibroDiario()
        diario.registrar_partida(
            fecha=data["fecha"],
            descripcion=data["descripcion"],
            cuenta_debe=data["cuenta_debe"],
            cuenta_haber=data["cuenta_haber"],
            monto=float(data["monto"]),
            tipo=data.get("tipo", "normal"),
        )
        return {"ok": True, "message": "Partida registrada"}

    @app.post("/api/partida-ajuste")
    def api_registrar_ajuste():
        """Endpoint específico para partidas de ajuste"""
        data = request.get_json()
        diario = sc.LibroDiario()
        diario.crear_partida_ajuste(
            fecha=data["fecha"],
            descripcion=data["descripcion"],
            cuenta_debe=data["cuenta_debe"],
            cuenta_haber=data["cuenta_haber"],
            monto=float(data["monto"]),
        )
        return {"ok": True, "message": "Partida de ajuste registrada"}
        payload: Dict[str, Any] = request.get_json(force=True)
        fecha = payload.get("fecha") or datetime.now().strftime("%Y-%m-%d")
        descripcion = payload.get("descripcion", "")
        cuenta_debe = payload.get("cuenta_debe", "")
        cuenta_haber = payload.get("cuenta_haber", "")
        monto = float(payload.get("monto", 0))

        diario = sc.LibroDiario()
        diario.registrar_partida(fecha, descripcion, cuenta_debe, cuenta_haber, monto)
        return {"ok": True}

    @app.post("/api/factura")
    def api_crear_factura():
        payload: Dict[str, Any] = request.get_json(force=True)
        cliente = payload.get("cliente", "")
        descripcion = payload.get("descripcion", "")
        monto = float(payload.get("monto", 0))

        fact = sc.Facturacion()
        fact.crear_factura(cliente, monto, descripcion)
        return {"ok": True}

    @app.get("/api/ventas")
    def api_reporte_ventas():
        fecha = request.args.get("fecha")
        fact = sc.Facturacion()
        ventas = fact.reporte_ventas_diarias(fecha)
        data = [
            {
                "id": v[0],
                "fecha": v[1],
                "cliente": v[2],
                "monto": v[3],
                "descripcion": v[4],
            }
            for v in ventas
        ]
        return jsonify(data)

    return app


def _run_flask(app: Flask, host: str = "127.0.0.1", port: int = 5000):
    app.run(host=host, port=port, debug=False, use_reloader=False)


def main():
    # Inicia Flask en un hilo y abre ventana pywebview
    app = create_app()

    t = threading.Thread(target=_run_flask, args=(app,), daemon=True)
    t.start()

    # Crea ventana desktop
    try:
        import webview

        window = webview.create_window(
            title="Sistema Contable",
            url="http://127.0.0.1:5000/",
            width=1200,
            height=800,
            resizable=True,
        )
        webview.start()
    except Exception as e:
        # Fallback: si no hay entorno gráfico, al menos dejar Flask sirviendo
        print(f"No se pudo iniciar la ventana nativa: {e}\n",
              "El servidor sigue disponible en http://127.0.0.1:5000")
        t.join()


if __name__ == "__main__":
    main()

# Exponer variable `app` para facilitar el uso de `flask run` en modo desarrollo
# Ejemplo:
#   source .venv/bin/activate
#   export FLASK_APP=app_ui.py
#   flask run --reload --debug
# Esto evita el hilo + pywebview y simplemente levanta el servidor para pruebas rápidas.
app = create_app()
