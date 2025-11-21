from base_datos import BaseDatos
from mayor import Mayorizacion

class EstadosFinancieros:
    def __init__(self):
        self.db = BaseDatos()
    
    def balanza_comprobacion(self):
        mayor = Mayorizacion()
        saldos = mayor.calcular_saldos_cuentas()
        
        print("\n--- BALANZA DE COMPROBACIÓN ---")
        total_debe = 0
        total_haber = 0
        
        for cuenta, movimientos in saldos.items():
            total_debe += movimientos['debe']
            total_haber += movimientos['haber']
            saldo = movimientos['debe'] - movimientos['haber']
            print(f"{cuenta}: Debe ${movimientos['debe']} | Haber ${movimientos['haber']} | Saldo ${saldo}")
        
        print(f"\nTOTAL DEBE: ${total_debe}")
        print(f"TOTAL HABER: ${total_haber}")
        print(f"DIFERENCIA: ${total_debe - total_haber}")
        
        return saldos
    
    def balance_general(self):
        saldos = self.balanza_comprobacion()
        
        print("\n--- BALANCE GENERAL ---")
        
        activos = 0
        pasivos = 0
        capital = 0
        
        # Obtener información de tipos de cuenta
        for cuenta in saldos.keys():
            tipo_info = self.db.obtener_datos(
                'SELECT tipo FROM catalogo_cuentas WHERE codigo = ?', 
                (cuenta,)
            )
            if tipo_info:
                tipo = tipo_info[0][0]
                saldo_cuenta = saldos[cuenta]['debe'] - saldos[cuenta]['haber']
                
                if tipo == 'Activo':
                    activos += saldo_cuenta
                elif tipo == 'Pasivo':
                    pasivos += saldo_cuenta
                elif tipo == 'Capital':
                    capital += saldo_cuenta
        
        print(f"TOTAL ACTIVOS: ${activos}")
        print(f"TOTAL PASIVOS: ${pasivos}")
        print(f"TOTAL CAPITAL: ${capital}")
        print(f"ACTIVOS = PASIVOS + CAPITAL: ${activos} = ${pasivos + capital}")