from base_datos import BaseDatos

class Mayor:
    def __init__(self):
        self.db = BaseDatos()

    def obtener_mayor_por_cuenta(self, cuenta_codigo):
        transacciones = self.db.obtener_datos(
            'SELECT * FROM libro_diario WHERE cuenta_debe = ? OR cuenta_haber = ? ORDER BY fecha',
            (cuenta_codigo, cuenta_codigo)
        )
        
        saldo = 0
        print(f"\n--- MAYOR DE LA CUENTA: {cuenta_codigo} ---")
        for trans in transacciones:
            fecha, desc, c_debe, c_haber, monto = trans[1], trans[2], trans[3], trans[4], trans[5]
            if c_debe == cuenta_codigo:
                saldo += monto
                print(f"Fecha: {fecha} | Desc: {desc} | Debe: ${monto} | Saldo: ${saldo}")
            else:
                saldo -= monto
                print(f"Fecha: {fecha} | Desc: {desc} | Haber: ${monto} | Saldo: ${saldo}")
        return saldo

    def mostrar_mayor_general(self):
        cuentas = self.db.obtener_datos('SELECT codigo FROM catalogo_cuentas')
        print("\n--- LIBRO MAYOR GENERAL ---")
        for cuenta in cuentas:
            self.obtener_mayor_por_cuenta(cuenta[0])