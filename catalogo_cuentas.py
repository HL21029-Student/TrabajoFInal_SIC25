from base_datos import BaseDatos

class CatalogoCuentas:
    def __init__(self):
        self.db = BaseDatos()
        self.crear_catalogo_base()
    
    def crear_catalogo_base(self):
        # Cuentas específicas para restaurante
        cuentas_base = [
            ('1', 'ACTIVO', 'Activo', 1),
            ('1.1', 'ACTIVO CORRIENTE', 'Activo', 2),
            ('1.1.1', 'Caja', 'Activo', 3),
            ('1.1.2', 'Bancos', 'Activo', 3),
            ('1.1.3', 'Clientes', 'Activo', 3),
            ('1.1.4', 'Inventario de Alimentos', 'Activo', 3),
            ('1.1.5', 'Inventario de Bebidas', 'Activo', 3),
            ('2', 'PASIVO', 'Pasivo', 1),
            ('2.1', 'PASIVO CORRIENTE', 'Pasivo', 2),
            ('2.1.1', 'Proveedores de Alimentos', 'Pasivo', 3),
            ('2.1.2', 'Proveedores de Bebidas', 'Pasivo', 3),
            ('2.1.3', 'Sueldos Pendientes', 'Pasivo', 3),
            ('3', 'CAPITAL', 'Capital', 1),
            ('4', 'INGRESOS', 'Ingreso', 1),
            ('4.1', 'Ventas de Comidas', 'Ingreso', 2),
            ('4.2', 'Ventas de Bebidas', 'Ingreso', 2),
            ('4.3', 'Ventas de Postres', 'Ingreso', 2),
            ('5', 'GASTOS', 'Gasto', 1),
            ('5.1', 'Gastos de Alimentos', 'Gasto', 2),
            ('5.2', 'Gastos de Bebidas', 'Gasto', 2),
            ('5.3', 'Sueldos y Salarios', 'Gasto', 2),
            ('5.4', 'Gastos de Servicios (Luz, Agua, etc.)', 'Gasto', 2),
            ('5.5', 'Gastos de Mantenimiento', 'Gasto', 2),
            ('5.6', 'Gastos Administrativos', 'Gasto', 2)
        ]
        
        for cuenta in cuentas_base:
            try:
                self.db.ejecutar_consulta(
                    'INSERT INTO catalogo_cuentas VALUES (?, ?, ?, ?)',
                    cuenta
                )
            except:
                pass  # La cuenta ya existe
        print("Catálogo de cuentas base verificado.")

    def agregar_cuenta(self, codigo, nombre, tipo, nivel):
        self.db.ejecutar_consulta(
            'INSERT INTO catalogo_cuentas VALUES (?, ?, ?, ?)',
            (codigo, nombre, tipo, nivel)
        )

    def obtener_cuenta(self, codigo):
        return self.db.obtener_datos('SELECT * FROM catalogo_cuentas WHERE codigo = ?', (codigo,))

    def mostrar_catalogo(self):
        cuentas = self.db.obtener_datos('SELECT * FROM catalogo_cuentas ORDER BY codigo')
        print("\n--- CATÁLOGO DE CUENTAS ---")
        for cuenta in cuentas:
            print(f"{cuenta[0]} - {cuenta[1]} ({cuenta[2]})")
        return cuentas