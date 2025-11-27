from base_datos import BaseDatos
from datetime import datetime

class Diario:
    def __init__(self):
        self.db = BaseDatos()

    def registrar_asiento(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo="normal"):
        # Validar que las cuentas existen
        if not self._cuenta_existe(cuenta_debe) or not self._cuenta_existe(cuenta_haber):
            print("Error: Una o ambas cuentas no existen en el catálogo.")
            return False
        
        self.db.ejecutar_consulta(
            '''INSERT INTO libro_diario
               (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo)
        )
        return True

    def mostrar_asientos(self):
        asientos = self.db.obtener_datos('SELECT * FROM libro_diario ORDER BY fecha, id')
        print("\n--- LIBRO DIARIO ---")
        for asiento in asientos:
            print(f"ID: {asiento[0]} | Fecha: {asiento[1]} | Desc: {asiento[2]} | Debe: {asiento[3]} | Haber: {asiento[4]} | Monto: ${asiento[5]}")
        return asientos

    def _cuenta_existe(self, codigo):
        cuenta = self.db.obtener_datos('SELECT * FROM catalogo_cuentas WHERE codigo = ?', (codigo,))
        return len(cuenta) > 0

    def registrar_ajuste(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto):
        return self.registrar_asiento(fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo="ajuste")