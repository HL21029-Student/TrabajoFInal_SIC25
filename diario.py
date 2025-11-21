from base_datos import BaseDatos
from datetime import datetime

class LibroDiario:
    def __init__(self):
        self.db = BaseDatos()
    
    def registrar_partida(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo="normal"):
        self.db.ejecutar_consulta(
            '''INSERT INTO libro_diario 
               (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo)
        )
        print("Partida registrada exitosamente!")
    
    def mostrar_diario(self):
        partidas = self.db.obtener_datos('SELECT * FROM libro_diario ORDER BY fecha, id')
        print("\n--- LIBRO DIARIO ---")
        for p in partidas:
            print(f"Fecha: {p[1]} | Desc: {p[2]} | Debe: {p[3]} | Haber: {p[4]} | Monto: ${p[5]}")
        return partidas
    
    def crear_partida_ajuste(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto):
        self.registrar_partida(fecha, descripcion, cuenta_debe, cuenta_haber, monto, "ajuste")