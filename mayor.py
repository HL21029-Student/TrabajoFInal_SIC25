from base_datos import BaseDatos

class Mayorizacion:
    def __init__(self):
        self.db = BaseDatos()
    
    def calcular_saldos_cuentas(self):
        # Obtener todas las transacciones
        transacciones = self.db.obtener_datos('SELECT * FROM libro_diario')
        
        saldos = {}
        
        for trans in transacciones:
            cuenta_debe = trans[3]
            cuenta_haber = trans[4]
            monto = trans[5]
            
            # Sumar al debe
            if cuenta_debe not in saldos:
                saldos[cuenta_debe] = {'debe': 0, 'haber': 0}
            saldos[cuenta_debe]['debe'] += monto
            
            # Sumar al haber
            if cuenta_haber not in saldos:
                saldos[cuenta_haber] = {'debe': 0, 'haber': 0}
            saldos[cuenta_haber]['haber'] += monto
        
        return saldos
    
    def mostrar_mayor(self):
        saldos = self.calcular_saldos_cuentas()
        print("\n--- LIBRO MAYOR ---")
        for cuenta, movimientos in saldos.items():
            saldo = movimientos['debe'] - movimientos['haber']
            print(f"Cuenta: {cuenta} | Debe: ${movimientos['debe']} | Haber: ${movimientos['haber']} | Saldo: ${saldo}")
        
        return saldos