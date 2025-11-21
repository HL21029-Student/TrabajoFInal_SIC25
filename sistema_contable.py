from catalogo_cuentas import CatalogoCuentas
from diario import LibroDiario
from mayor import Mayorizacion
from estados_financieros import EstadosFinancieros
from facturacion import Facturacion
from datetime import datetime

class SistemaContable:
    def __init__(self):
        self.catalogo = CatalogoCuentas()
        self.diario = LibroDiario()
        self.mayor = Mayorizacion()
        self.estados = EstadosFinancieros()
        self.facturacion = Facturacion()
    
    def mostrar_menu(self):
        while True:
            print("\n" + "="*50)
            print("        SISTEMA CONTABLE INTEGRAL")
            print("="*50)
            print("1. Catálogo de Cuentas")
            print("2. Manual de Cuentas")
            print("3. Libro Diario")
            print("4. Libro Mayor")
            print("5. Partidas de Ajuste")
            print("6. Balanza de Comprobación")
            print("7. Balance General")
            print("8. Estados Financieros")
            print("9. Facturación")
            print("10. Reporte de Ventas")
            print("0. Salir")
            print("="*50)
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.mostrar_catalogo()
            elif opcion == "2":
                self.mostrar_manual()
            elif opcion == "3":
                self.gestionar_diario()
            elif opcion == "4":
                self.mostrar_mayor()
            elif opcion == "5":
                self.crear_ajuste()
            elif opcion == "6":
                self.mostrar_balanza()
            elif opcion == "7":
                self.mostrar_balance()
            elif opcion == "8":
                self.mostrar_estados_financieros()
            elif opcion == "9":
                self.crear_factura()
            elif opcion == "10":
                self.mostrar_reporte_ventas()
            elif opcion == "0":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
    
    def mostrar_catalogo(self):
        self.catalogo.mostrar_catalogo()
    
    def mostrar_manual(self):
        print("\n--- MANUAL DE CUENTAS ---")
        print("Este manual explica el uso de cada cuenta:")
        print("1.1.1 Caja: Controla el efectivo en caja")
        print("1.1.2 Bancos: Controla saldos bancarios")
        print("1.1.3 Clientes: Cuentas por cobrar a clientes")
        print("2.1.1 Proveedores: Cuentas por pagar a proveedores")
        print("4.1 Ventas: Ingresos por ventas de productos")
        print("5.1 Gastos Administrativos: Gastos de operación")
    
    def gestionar_diario(self):
        print("\n--- LIBRO DIARIO ---")
        print("1. Ver partidas existentes")
        print("2. Registrar nueva partida")
        
        opcion = input("Selecciona: ")
        if opcion == "1":
            self.diario.mostrar_diario()
        elif opcion == "2":
            fecha = input("Fecha (YYYY-MM-DD): ")
            descripcion = input("Descripción: ")
            cuenta_debe = input("Cuenta Debe (ej: 1.1.1): ")
            cuenta_haber = input("Cuenta Haber (ej: 4.1): ")
            monto = float(input("Monto: "))
            
            self.diario.registrar_partida(fecha, descripcion, cuenta_debe, cuenta_haber, monto)
    
    def mostrar_mayor(self):
        self.mayor.mostrar_mayor()
    
    def crear_ajuste(self):
        print("\n--- PARTIDA DE AJUSTE ---")
        fecha = input("Fecha (YYYY-MM-DD): ")
        descripcion = input("Descripción del ajuste: ")
        cuenta_debe = input("Cuenta Debe: ")
        cuenta_haber = input("Cuenta Haber: ")
        monto = float(input("Monto: "))
        
        self.diario.crear_partida_ajuste(fecha, descripcion, cuenta_debe, cuenta_haber, monto)
    
    def mostrar_balanza(self):
        self.estados.balanza_comprobacion()
    
    def mostrar_balance(self):
        self.estados.balance_general()
    
    def mostrar_estados_financieros(self):
        print("\n--- ESTADOS FINANCIEROS COMPLETOS ---")
        self.estados.balanza_comprobacion()
        self.estados.balance_general()
    
    def crear_factura(self):
        print("\n--- FACTURACIÓN ---")
        cliente = input("Nombre del cliente: ")
        descripcion = input("Descripción del producto/servicio: ")
        monto = float(input("Monto total: "))
        
        self.facturacion.crear_factura(cliente, monto, descripcion)
    
    def mostrar_reporte_ventas(self):
        fecha = input("Fecha para reporte (YYYY-MM-DD) o Enter para hoy: ")
        if fecha == "":
            self.facturacion.reporte_ventas_diarias()
        else:
            self.facturacion.reporte_ventas_diarias(fecha)

# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaContable()
    sistema.mostrar_menu()