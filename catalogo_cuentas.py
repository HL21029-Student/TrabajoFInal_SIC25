from base_datos import BaseDatos

class CatalogoCuentas:
    def __init__(self):
        self.db = BaseDatos()
        self.crear_catalogo_base()
    
    def crear_catalogo_base(self):
        # Cuentas básicas del catálogo
        cuentas_base = [
            ('1', 'ACTIVO', 'Activo', 1),
            ('1.1', 'ACTIVO CORRIENTE', 'Activo', 2),
            ('1.1.1', 'Caja', 'Activo', 3),
            ('1.1.2', 'Bancos', 'Activo', 3),
            ('1.1.3', 'Clientes', 'Activo', 3),
            ('2', 'PASIVO', 'Pasivo', 1),
            ('2.1', 'PASIVO CORRIENTE', 'Pasivo', 2),
            ('2.1.1', 'Proveedores', 'Pasivo', 3),
            ('3', 'CAPITAL', 'Capital', 1),
            ('4', 'INGRESOS', 'Ingreso', 1),
            ('4.1', 'Ventas', 'Ingreso', 2),
            ('5', 'GASTOS', 'Gasto', 1),
            ('5.1', 'Gastos Administrativos', 'Gasto', 2)
        ]
        
        for cuenta in cuentas_base:
            try:
                self.db.ejecutar_consulta(
                    'INSERT INTO catalogo_cuentas VALUES (?, ?, ?, ?)',
                    cuenta
                )
            except:
                pass  # La cuenta ya existe
    
    def agregar_cuenta(self, codigo, nombre, tipo, nivel):
        self.db.ejecutar_consulta(
            'INSERT INTO catalogo_cuentas VALUES (?, ?, ?, ?)',
            (codigo, nombre, tipo, nivel)
        )
    
    def mostrar_catalogo(self):
        cuentas = self.db.obtener_datos('SELECT * FROM catalogo_cuentas ORDER BY codigo')
        print("\n--- CATÁLOGO DE CUENTAS ---")
        for cuenta in cuentas:
            print(f"{cuenta[0]} - {cuenta[1]} ({cuenta[2]})")
        return cuentas