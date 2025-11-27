from catalogo_cuentas import CatalogoCuentas
from diario import Diario
from mayor import Mayor
from estados_financieros import EstadosFinancieros
from facturacion import Facturacion
from manual_cuentas import ManualCuentas
from balanza import Balanza
from balance_inicial import BalanceInicial

class SistemaContable:
    def __init__(self):
        self.catalogo = CatalogoCuentas()
        self.diario = Diario()
        self.mayor = Mayor()
        self.estados = EstadosFinancieros()
        self.facturacion = Facturacion()
        self.manual = ManualCuentas()
        self.balanza = Balanza()
        self.balance_inicial = BalanceInicial()

    def menu_principal(self):
        while True:
            print("\n=== SISTEMA CONTABLE PARA RESTAURANTE ===")
            print("1. Gestión de Catálogo de Cuentas")
            print("2. Gestión de Manual de Cuentas")
            print("3. Balance Inicial")
            print("4. Registro en Libro Diario")
            print("5. Partidas de Ajuste")
            print("6. Consulta de Libro Mayor")
            print("7. Balanza de Comprobación")
            print("8. Estados Financieros")
            print("9. Facturación y Pedidos")
            print("10. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.menu_catalogo()
            elif opcion == '2':
                self.menu_manual()
            elif opcion == '3':
                self.balance_inicial.registrar_balance_inicial()
            elif opcion == '4':
                self.menu_diario()
            elif opcion == '5':
                self.menu_ajustes()
            elif opcion == '6':
                self.menu_mayor()
            elif opcion == '7':
                self.balanza.mostrar_balanza()
            elif opcion == '8':
                self.menu_estados()
            elif opcion == '9':
                self.menu_facturacion()
            elif opcion == '10':
                break
            else:
                print("Opción no válida.")

    def menu_catalogo(self):
        while True:
            print("\n--- GESTIÓN DE CATÁLOGO DE CUENTAS ---")
            print("1. Mostrar Catálogo")
            print("2. Agregar Cuenta")
            print("3. Buscar Cuenta por Código")
            print("4. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.catalogo.mostrar_catalogo()
            elif opcion == '2':
                codigo = input("Código: ")
                nombre = input("Nombre: ")
                tipo = input("Tipo (Activo/Pasivo/Capital/Ingreso/Gasto): ")
                nivel = int(input("Nivel: "))
                self.catalogo.agregar_cuenta(codigo, nombre, tipo, nivel)
                print("Cuenta agregada exitosamente.")
            elif opcion == '3':
                codigo = input("Código de la cuenta a buscar: ")
                cuenta = self.catalogo.obtener_cuenta(codigo)
                if cuenta:
                    print(f"Cuenta encontrada: {cuenta[0][0]} - {cuenta[0][1]} ({cuenta[0][2]})")
                else:
                    print("Cuenta no encontrada.")
            elif opcion == '4':
                break
            else:
                print("Opción no válida.")

    def menu_manual(self):
        while True:
            print("\n--- GESTIÓN DE MANUAL DE CUENTAS ---")
            print("1. Mostrar Manual")
            print("2. Agregar Descripción a Cuenta")
            print("3. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.manual.mostrar_manual()
            elif opcion == '2':
                codigo = input("Código de la cuenta: ")
                descripcion = input("Descripción de la cuenta: ")
                self.manual.agregar_descripcion(codigo, descripcion)
                print("Descripción agregada exitosamente.")
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_diario(self):
        while True:
            print("\n--- REGISTRO EN LIBRO DIARIO ---")
            print("1. Registrar Asiento")
            print("2. Mostrar Asientos")
            print("3. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                fecha = input("Fecha (YYYY-MM-DD): ")
                descripcion = input("Descripción: ")
                self.catalogo.mostrar_catalogo()
                cuenta_debe = input("Cuenta Débito: ")
                cuenta_haber = input("Cuenta Crédito: ")
                monto = float(input("Monto: "))
                tipo = input("Tipo (venta/compra/etc.): ")
                if self.diario.registrar_asiento(fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo):
                    print("Asiento registrado exitosamente.")
            elif opcion == '2':
                self.diario.mostrar_asientos()
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_ajustes(self):
        while True:
            print("\n--- PARTIDAS DE AJUSTE ---")
            print("1. Registrar Partida de Ajuste")
            print("2. Ver Partidas de Ajuste")
            print("3. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                fecha = input("Fecha (YYYY-MM-DD): ")
                descripcion = input("Descripción: ")
                self.catalogo.mostrar_catalogo()
                cuenta_debe = input("Cuenta Débito: ")
                cuenta_haber = input("Cuenta Crédito: ")
                monto = float(input("Monto: "))
                if self.diario.registrar_ajuste(fecha, descripcion, cuenta_debe, cuenta_haber, monto):
                    print("Partida de ajuste registrada exitosamente.")
            elif opcion == '2':
                ajustes = self.diario.db.obtener_datos("SELECT * FROM libro_diario WHERE tipo = 'ajuste'")
                for ajuste in ajustes:
                    print(f"ID: {ajuste[0]} | Fecha: {ajuste[1]} | Desc: {ajuste[2]} | Debe: {ajuste[3]} | Haber: {ajuste[4]} | Monto: ${ajuste[5]}")
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_mayor(self):
        while True:
            print("\n--- CONSULTA DE LIBRO MAYOR ---")
            print("1. Mostrar Mayor por Cuenta Específica")
            print("2. Mostrar Mayor General")
            print("3. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.catalogo.mostrar_catalogo()
                cuenta = input("Código de la cuenta: ")
                self.mayor.obtener_mayor_por_cuenta(cuenta)
            elif opcion == '2':
                self.mayor.mostrar_mayor_general()
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_estados(self):
        while True:
            print("\n--- ESTADOS FINANCIEROS ---")
            print("1. Balance General")
            print("2. Estado de Resultados")
            print("3. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.estados.balance_general()
            elif opcion == '2':
                self.estados.estado_resultados()
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_facturacion(self):
        while True:
            print("\n--- FACTURACIÓN Y PEDIDOS ---")
            print("1. Crear Pedido/Factura")
            print("2. Mostrar Factura")
            print("3. Listar Facturas")
            print("4. Mostrar Menú del Restaurante")
            print("5. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                cliente = input("Nombre del cliente: ")
                factura_id = self.facturacion.crear_factura(cliente)
                if factura_id:
                    print(f"Pedido/Factura #{factura_id} creado exitosamente.")
            elif opcion == '2':
                factura_id = int(input("ID de Factura: "))
                self.facturacion.mostrar_factura(factura_id)
            elif opcion == '3':
                self.facturacion.listar_facturas()
            elif opcion == '4':
                self.facturacion.mostrar_menu_restaurante()
            elif opcion == '5':
                break
            else:
                print("Opción no válida.")

if __name__ == '__main__':
    sistema = SistemaContable()
    sistema.menu_principal()
