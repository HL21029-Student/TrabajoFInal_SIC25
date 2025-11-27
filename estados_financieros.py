from base_datos import BaseDatos
from balanza import Balanza

class EstadosFinancieros:
    def __init__(self):
        self.db = BaseDatos()
        self.balanza = Balanza()

    def balance_general(self):
        saldos = self.balanza.calcular_saldos()
        
        activos = {}
        pasivos = {}
        capital = {}

        for codigo, data in saldos.items():
            tipo_info = self.db.obtener_datos('SELECT tipo FROM catalogo_cuentas WHERE codigo = ?', (codigo,))
            if tipo_info:
                tipo = tipo_info[0][0]
                saldo = data['debe'] - data['haber']
                if tipo == 'Activo':
                    activos[codigo] = {'nombre': data['nombre'], 'saldo': saldo}
                elif tipo == 'Pasivo':
                    pasivos[codigo] = {'nombre': data['nombre'], 'saldo': -saldo}
                elif tipo == 'Capital':
                    capital[codigo] = {'nombre': data['nombre'], 'saldo': -saldo}

        total_activos = sum(d['saldo'] for d in activos.values())
        total_pasivos = sum(d['saldo'] for d in pasivos.values())
        total_capital = sum(d['saldo'] for d in capital.values())

        print("\n--- BALANCE GENERAL ---")
        print("\nACTIVOS")
        for codigo, data in activos.items():
            print(f"{codigo} {data['nombre']:<30} {data['saldo']:15.2f}")
        print(f"{'Total Activos':<31} {total_activos:15.2f}")

        print("\nPASIVOS")
        for codigo, data in pasivos.items():
            print(f"{codigo} {data['nombre']:<30} {data['saldo']:15.2f}")
        print(f"{'Total Pasivos':<31} {total_pasivos:15.2f}")

        print("\nCAPITAL")
        for codigo, data in capital.items():
            print(f"{codigo} {data['nombre']:<30} {data['saldo']:15.2f}")
        print(f"{'Total Capital':<31} {total_capital:15.2f}")

        print("\n--- VERIFICACIÓN ---")
        print(f"Total Pasivo + Capital: {total_pasivos + total_capital:15.2f}")
        print(f"Total Activo:           {total_activos:15.2f}")

    def estado_resultados(self):
        saldos = self.balanza.calcular_saldos()
        
        ingresos = {}
        gastos = {}

        for codigo, data in saldos.items():
            tipo_info = self.db.obtener_datos('SELECT tipo FROM catalogo_cuentas WHERE codigo = ?', (codigo,))
            if tipo_info:
                tipo = tipo_info[0][0]
                saldo = data['debe'] - data['haber']
                if tipo == 'Ingreso':
                    ingresos[codigo] = {'nombre': data['nombre'], 'saldo': -saldo}
                elif tipo == 'Gasto':
                    gastos[codigo] = {'nombre': data['nombre'], 'saldo': saldo}

        total_ingresos = sum(d['saldo'] for d in ingresos.values())
        total_gastos = sum(d['saldo'] for d in gastos.values())
        utilidad = total_ingresos - total_gastos

        print("\n--- ESTADO DE RESULTADOS ---")
        print("\nINGRESOS")
        for codigo, data in ingresos.items():
            print(f"{codigo} {data['nombre']:<30} {data['saldo']:15.2f}")
        print(f"{'Total Ingresos':<31} {total_ingresos:15.2f}")

        print("\nGASTOS")
        for codigo, data in gastos.items():
            print(f"{codigo} {data['nombre']:<30} {data['saldo']:15.2f}")
        print(f"{'Total Gastos':<31} {total_gastos:15.2f}")

        print("\n--- RESULTADO ---")
        print(f"Utilidad Neta: {utilidad:15.2f}")