from base_datos import BaseDatos

class ManualCuentas:
    def __init__(self):
        self.db = BaseDatos()

    def agregar_descripcion(self, codigo, descripcion):
        self.db.ejecutar_consulta(
            'INSERT INTO manual_cuentas VALUES (?, ?)',
            (codigo, descripcion)
        )

    def obtener_descripcion(self, codigo):
        return self.db.obtener_datos('SELECT descripcion FROM manual_cuentas WHERE codigo = ?', (codigo,))

    def mostrar_manual(self):
        manual = self.db.obtener_datos('SELECT mc.codigo, cc.nombre, mc.descripcion FROM manual_cuentas mc JOIN catalogo_cuentas cc ON mc.codigo = cc.codigo ORDER BY mc.codigo')
        print("\n--- MANUAL DE CUENTAS ---")
        for cuenta in manual:
            print(f"{cuenta[0]} - {cuenta[1]}: {cuenta[2]}")
        return manual