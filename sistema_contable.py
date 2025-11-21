from catalogo_cuentas import CatalogoCuentas
from diario import Diario
from mayor import Mayor
from estados_financieros import EstadosFinancieros
from facturacion import Facturacion

class SistemaContable:
    def __init__(self):
        self.catalogo = CatalogoCuentas()
        self.diario = Diario()
        self.mayor = Mayor()
        self.estados = EstadosFinancieros()
        self.facturacion = Facturacion()

    def menu_principal(self):
        while True:
            print("\n=== SISTEMA CONTABLE PARA RESTAURANTE ===")
            print("1. Gestión de Catálogo de Cuentas")
            print("2. Registro en Libro Diario")
            print("3. Consulta de Libro Mayor")
            print("4. Estados Financieros")
            print("5. Facturación y Pedidos")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.menu_catalogo()
            elif opcion == '2':
                self.menu_diario()
            elif opcion == '3':
                self.menu_mayor()
            elif opcion == '4':
                self.menu_estados()
            elif opcion == '5':
                self.menu_facturacion()
            elif opcion == '6':
                break
            else:
                print("Opción no válida.")

    def menu_catalogo(self):
        while True:
            print("\n--- GESTIÓN DE CATÁLOGO DE CUENTAS ---")
            print("1. Mostrar Catálogo")
            print("2. Agregar Cuenta")
            print("3. Volver al Menú Principal")

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
                cuenta_debe = input("Cuenta Débito: ")
                cuenta_haber = input("Cuenta Crédito: ")
                monto = float(input("Monto: "))
                tipo = input("Tipo (venta/compra/etc.): ")
                self.diario.registrar_asiento(fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo)
                print("Asiento registrado exitosamente.")
            elif opcion == '2':
                self.diario.mostrar_asientos()
            elif opcion == '3':
                break
            else:
                print("Opción no válida.")

    def menu_mayor(self):
        while True:
            print("\n--- CONSULTA DE LIBRO MAYOR ---")
            print("1. Mostrar Mayor por Cuenta")
            print("2. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                cuenta = input("Cuenta: ")
                self.mayor.mostrar_mayor_cuenta(cuenta)
            elif opcion == '2':
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
