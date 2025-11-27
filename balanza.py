from base_datos import BaseDatos

class Balanza:
    def __init__(self):
        self.db = BaseDatos()

    def calcular_saldos(self):
        cuentas = self.db.obtener_datos('SELECT codigo, nombre FROM catalogo_cuentas')
        saldos = {cuenta[0]: {'nombre': cuenta[1], 'debe': 0, 'haber': 0} for cuenta in cuentas}

        transacciones = self.db.obtener_datos('SELECT cuenta_debe, cuenta_haber, monto FROM libro_diario')
        for trans in transacciones:
            cuenta_debe, cuenta_haber, monto = trans[0], trans[1], trans[2]
            if cuenta_debe in saldos:
                saldos[cuenta_debe]['debe'] += monto
            if cuenta_haber in saldos:
                saldos[cuenta_haber]['haber'] += monto
        
        return saldos

    def mostrar_balanza(self):
        saldos = self.calcular_saldos()
        total_debe = 0
        total_haber = 0

        print("\n--- BALANZA DE COMPROBACIÓN ---")
        print(f"{'Código':<10} | {'Cuenta':<30} | {'Debe':>15} | {'Haber':>15}")
        print("-" * 75)

        for codigo, data in sorted(saldos.items()):
            debe = data['debe']
            haber = data['haber']
            saldo_final = debe - haber

            if saldo_final > 0:
                print(f"{codigo:<10} | {data['nombre']:<30} | {saldo_final:15.2f} | {'':>15}")
                total_debe += saldo_final
            else:
                print(f"{codigo:<10} | {data['nombre']:<30} | {'':>15} | {-saldo_final:15.2f}")
                total_haber += -saldo_final

        print("-" * 75)
        print(f"{'TOTAL':<43} | {total_debe:15.2f} | {total_haber:15.2f}")

        if abs(total_debe - total_haber) < 0.01:
            print("\nLa balanza está cuadrada.")
        else:
            print("\n¡La balanza NO está cuadrada!")