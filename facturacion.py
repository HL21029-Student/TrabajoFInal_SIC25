from base_datos import BaseDatos
from datetime import datetime
from diario import LibroDiario

class Facturacion:
    def __init__(self):
        self.db = BaseDatos()
    
    def crear_factura(self, cliente, monto, descripcion):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        self.db.ejecutar_consulta(
            'INSERT INTO facturas (fecha, cliente, monto, descripcion) VALUES (?, ?, ?, ?)',
            (fecha_actual, cliente, monto, descripcion)
        )
        
        # Registrar en el diario (venta)
        diario = LibroDiario()
        diario.registrar_partida(
            fecha_actual, 
            f"Venta a {cliente} - {descripcion}",
            "1.1.1",  # Caja (asumiendo pago en efectivo)
            "4.1",    # Ventas
            monto
        )
        
        print(f"\n--- FACTURA GENERADA ---")
        print(f"Cliente: {cliente}")
        print(f"Fecha: {fecha_actual}")
        print(f"Descripción: {descripcion}")
        print(f"Monto: ${monto}")
        print("------------------------")
    
    def reporte_ventas_diarias(self, fecha=None):
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        ventas = self.db.obtener_datos(
            'SELECT * FROM facturas WHERE fecha = ?', 
            (fecha,)
        )
        
        print(f"\n--- REPORTE DE VENTAS DIARIAS ({fecha}) ---")
        total_dia = 0
        for venta in ventas:
            print(f"Cliente: {venta[2]} | Monto: ${venta[3]} | Desc: {venta[4]}")
            total_dia += venta[3]
        
        print(f"TOTAL DEL DÍA: ${total_dia}")
        return ventas