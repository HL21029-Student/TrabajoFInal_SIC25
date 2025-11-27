from base_datos import BaseDatos
from diario import Diario
from datetime import datetime

class BalanceInicial:
    def __init__(self):
        self.db = BaseDatos()
        self.diario = Diario()

    def registrar_balance_inicial(self):
        print("\n--- REGISTRO DE BALANCE INICIAL ---")
        fecha = datetime.now().strftime('%Y-%m-%d')
        
        # Cuentas de Activo
        print("\n--- Cuentas de Activo ---")
        total_activos = 0
        while True:
            cuenta = input("Cuenta de Activo (o 'fin' para terminar): ")
            if cuenta.lower() == 'fin':
                break
            monto = float(input(f"Saldo para {cuenta}: "))
            self.diario.registrar_asiento(fecha, "Balance Inicial", cuenta, "3.1.1", monto) # 3.1.1 es Capital Social
            total_activos += monto

        # Cuentas de Pasivo
        print("\n--- Cuentas de Pasivo ---")
        total_pasivos = 0
        while True:
            cuenta = input("Cuenta de Pasivo (o 'fin' para terminar): ")
            if cuenta.lower() == 'fin':
                break
            monto = float(input(f"Saldo para {cuenta}: "))
            self.diario.registrar_asiento(fecha, "Balance Inicial", "3.1.1", cuenta, monto) # 3.1.1 es Capital Social
            total_pasivos += monto
            
        # Cuentas de Capital (además del capital social)
        print("\n--- Cuentas de Capital ---")
        total_capital_adicional = 0
        while True:
            cuenta = input("Cuenta de Capital (o 'fin' para terminar): ")
            if cuenta.lower() == 'fin':
                break
            monto = float(input(f"Saldo para {cuenta}: "))
            self.diario.registrar_asiento(fecha, "Balance Inicial", "3.1.1", cuenta, monto) # 3.1.1 es Capital Social
            total_capital_adicional += monto

        # Calcular Capital Social
        capital_social = total_activos - total_pasivos - total_capital_adicional
        print(f"\nEl Capital Social calculado es: {capital_social}")
        
        print("\nBalance Inicial registrado exitosamente.")