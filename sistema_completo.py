#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime

# =============================================================================
# BASE DE DATOS
# =============================================================================

class BaseDatos:
    def __init__(self):
        self.conn = sqlite3.connect('sistema_contable.db')
        self.crear_tablas()
    
    def crear_tablas(self):
        cursor = self.conn.cursor()
        
        # Tabla para el catálogo de cuentas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalogo_cuentas (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                nivel INTEGER NOT NULL
            )
        ''')
        
        # Tabla para el libro diario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libro_diario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                cuenta_debe TEXT NOT NULL,
                cuenta_haber TEXT NOT NULL,
                monto REAL NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')
        
        # Tabla para facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                cliente TEXT NOT NULL,
                monto REAL NOT NULL,
                descripcion TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
    
    def ejecutar_consulta(self, consulta, parametros=()):
        cursor = self.conn.cursor()
        cursor.execute(consulta, parametros)
        self.conn.commit()
        return cursor
    
    def obtener_datos(self, consulta, parametros=()):
        cursor = self.conn.cursor()
        cursor.execute(consulta, parametros)
        return cursor.fetchall()

# =============================================================================
# CATÁLOGO DE CUENTAS
# =============================================================================

class CatalogoCuentas:
    def __init__(self):
        self.db = BaseDatos()
        self.crear_catalogo_base()
    
    def crear_catalogo_base(self):
        cuentas_base = [
            ('1', 'ACTIVO', 'Activo', 1),
            ('1.1', 'ACTIVO CORRIENTE', 'Activo', 2),
            ('1.1.1', 'Caja', 'Activo', 3),
            ('1.1.2', 'Bancos', 'Activo', 3),
            ('1.1.3', 'Clientes', 'Activo', 3),
            ('2', 'PASIVO', 'Pasivo', 1),
            ('2.1', 'PASIVO CORRIENTE', 'Pasivo', 2),
            ('2.1.1', 'Proveedores', 'Pasivo', 3),
            ('3', 'CAPITAL', 'Capital', 1),
            ('4', 'INGRESOS', 'Ingreso', 1),
            ('4.1', 'Ventas', 'Ingreso', 2),
            ('5', 'GASTOS', 'Gasto', 1),
            ('5.1', 'Gastos Administrativos', 'Gasto', 2)
        ]
        
        for cuenta in cuentas_base:
            try:
                self.db.ejecutar_consulta(
                    'INSERT OR IGNORE INTO catalogo_cuentas VALUES (?, ?, ?, ?)',
                    cuenta
                )
            except:
                pass
    
    def mostrar_catalogo(self):
        cuentas = self.db.obtener_datos('SELECT * FROM catalogo_cuentas ORDER BY codigo')
        print("\n" + "="*50)
        print("           CATÁLOGO DE CUENTAS")
        print("="*50)
        for cuenta in cuentas:
            print(f"{cuenta[0]} - {cuenta[1]} ({cuenta[2]}) - Nivel {cuenta[3]}")
        print("="*50)
        return cuentas

# =============================================================================
# LIBRO DIARIO
# =============================================================================

class LibroDiario:
    def __init__(self):
        self.db = BaseDatos()
    
    def registrar_partida(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo="normal"):
        self.db.ejecutar_consulta(
            '''INSERT INTO libro_diario 
               (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (fecha, descripcion, cuenta_debe, cuenta_haber, monto, tipo)
        )
        print("✅ Partida registrada exitosamente!")
    
    def mostrar_diario(self):
        partidas = self.db.obtener_datos('SELECT * FROM libro_diario ORDER BY fecha, id')
        print("\n" + "="*60)
        print("                     LIBRO DIARIO")
        print("="*60)
        print("Fecha      | Descripción                | Debe      | Haber     | Monto")
        print("-" * 60)
        for p in partidas:
            print(f"{p[1]:10} | {p[2]:25} | {p[3]:9} | {p[4]:9} | ${p[5]:.2f}")
        print("="*60)
        return partidas
    
    def crear_partida_ajuste(self, fecha, descripcion, cuenta_debe, cuenta_haber, monto):
        self.registrar_partida(fecha, descripcion, cuenta_debe, cuenta_haber, monto, "ajuste")
        print("✅ Partida de ajuste creada exitosamente!")

# =============================================================================
# MAYORIZACIÓN
# =============================================================================

class Mayorizacion:
    def __init__(self):
        self.db = BaseDatos()
    
    def calcular_saldos_cuentas(self):
        transacciones = self.db.obtener_datos('SELECT * FROM libro_diario')
        saldos = {}
        
        for trans in transacciones:
            cuenta_debe = trans[3]
            cuenta_haber = trans[4]
            monto = trans[5]
            
            if cuenta_debe not in saldos:
                saldos[cuenta_debe] = {'debe': 0, 'haber': 0}
            saldos[cuenta_debe]['debe'] += monto
            
            if cuenta_haber not in saldos:
                saldos[cuenta_haber] = {'debe': 0, 'haber': 0}
            saldos[cuenta_haber]['haber'] += monto
        
        return saldos
    
    def mostrar_mayor(self):
        saldos = self.calcular_saldos_cuentas()
        print("\n" + "="*70)
        print("                         LIBRO MAYOR")
        print("="*70)
        print("Cuenta     | Debe         | Haber        | Saldo")
        print("-" * 70)
        for cuenta, movimientos in saldos.items():
            saldo = movimientos['debe'] - movimientos['haber']
            print(f"{cuenta:10} | ${movimientos['debe']:11.2f} | ${movimientos['haber']:11.2f} | ${saldo:11.2f}")
        print("="*70)
        return saldos

# =============================================================================
# ESTADOS FINANCIEROS
# =============================================================================

class EstadosFinancieros:
    def __init__(self):
        self.db = BaseDatos()
    
    def balanza_comprobacion(self):
        mayor = Mayorizacion()
        saldos = mayor.calcular_saldos_cuentas()
        
        print("\n" + "="*70)
        print("                   BALANZA DE COMPROBACIÓN")
        print("="*70)
        total_debe = 0
        total_haber = 0
        
        for cuenta, movimientos in saldos.items():
            total_debe += movimientos['debe']
            total_haber += movimientos['haber']
            saldo = movimientos['debe'] - movimientos['haber']
            print(f"{cuenta:10} | Debe: ${movimientos['debe']:11.2f} | Haber: ${movimientos['haber']:11.2f} | Saldo: ${saldo:11.2f}")
        
        print("-" * 70)
        print(f"{'TOTAL':10} | Debe: ${total_debe:11.2f} | Haber: ${total_haber:11.2f} | Diferencia: ${total_debe - total_haber:11.2f}")
        print("="*70)
        
        return saldos
    
    def balance_general(self):
        saldos = self.balanza_comprobacion()
        
        print("\n" + "="*50)
        print("               BALANCE GENERAL")
        print("="*50)
        
        activos = 0
        pasivos = 0
        capital = 0
        
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
        
        print(f"ACTIVOS TOTALES:    ${activos:15.2f}")
        print(f"PASIVOS TOTALES:    ${pasivos:15.2f}")
        print(f"CAPITAL TOTAL:      ${capital:15.2f}")
        print("-" * 50)
        print(f"ECUACIÓN CONTABLE:  ${activos:15.2f} = ${pasivos + capital:15.2f}")
        
        if activos == pasivos + capital:
            print("✅ BALANCE CUADRADO CORRECTAMENTE")
        else:
            print("❌ ERROR: EL BALANCE NO CUADRA")
        print("="*50)

# =============================================================================
# FACTURACIÓN
# =============================================================================

class Facturacion:
    def __init__(self):
        self.db = BaseDatos()
    
    def crear_factura(self, cliente, monto, descripcion):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        self.db.ejecutar_consulta(
            'INSERT INTO facturas (fecha, cliente, monto, descripcion) VALUES (?, ?, ?, ?)',
            (fecha_actual, cliente, monto, descripcion)
        )
        
        diario = LibroDiario()
        diario.registrar_partida(
            fecha_actual, 
            f"Venta a {cliente} - {descripcion}",
            "1.1.1",
            "4.1",
            monto
        )
        
        print(f"\n" + "="*40)
        print("          FACTURA GENERADA")
        print("="*40)
        print(f"Cliente:    {cliente}")
        print(f"Fecha:      {fecha_actual}")
        print(f"Descripción: {descripcion}")
        print(f"Monto:      ${monto:.2f}")
        print("="*40)
    
    def reporte_ventas_diarias(self, fecha=None):
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        ventas = self.db.obtener_datos(
            'SELECT * FROM facturas WHERE fecha = ?', 
            (fecha,)
        )
        
        print(f"\n" + "="*50)
        print(f"     REPORTE DE VENTAS DIARIAS ({fecha})")
        print("="*50)
        total_dia = 0
        for venta in ventas:
            print(f"Cliente: {venta[2]:20} | ${venta[3]:10.2f} | {venta[4]}")
            total_dia += venta[3]
        
        print("-" * 50)
        print(f"TOTAL DEL DÍA: ${total_dia:33.2f}")
        print("="*50)
        return ventas

# =============================================================================
# SISTEMA PRINCIPAL
# =============================================================================

class SistemaContable:
    def __init__(self):
        self.catalogo = CatalogoCuentas()
        self.diario = LibroDiario()
        self.mayor = Mayorizacion()
        self.estados = EstadosFinancieros()
        self.facturacion = Facturacion()
    
    def mostrar_menu(self):
        while True:
            print("\n" + "="*60)
            print("           SISTEMA CONTABLE INTEGRAL - DEBIAN")
            print("="*60)
            print("1. 📋 Catálogo de Cuentas")
            print("2. 📖 Manual de Cuentas")
            print("3. 📒 Libro Diario")
            print("4. 📊 Libro Mayor")
            print("5. 🔧 Partidas de Ajuste")
            print("6. ⚖️ Balanza de Comprobación")
            print("7. 💼 Balance General")
            print("8. 📈 Estados Financieros")
            print("9. 🧾 Facturación")
            print("10. 📊 Reporte de Ventas")
            print("0. 🚪 Salir")
            print("="*60)
            
            opcion = input("Selecciona una opción (0-10): ").strip()
            
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
                print("\n¡Gracias por usar el Sistema Contable! 👋")
                break
            else:
                print("❌ Opción no válida. Por favor, selecciona una opción del 0 al 10.")
    
    def mostrar_catalogo(self):
        print("\n📋 CARGANDO CATÁLOGO DE CUENTAS...")
        self.catalogo.mostrar_catalogo()
        input("\nPresiona Enter para continuar...")
    
    def mostrar_manual(self):
        print("\n" + "="*50)
        print("           MANUAL DE CUENTAS")
        print("="*50)
        print("1.1.1 Caja: Controla el efectivo disponible en caja")
        print("1.1.2 Bancos: Controla los saldos en cuentas bancarias")
        print("1.1.3 Clientes: Representa las cuentas por cobrar a clientes")
        print("2.1.1 Proveedores: Representa las cuentas por pagar a proveedores")
        print("4.1 Ventas: Registra los ingresos por ventas de productos/servicios")
        print("5.1 Gastos Administrativos: Controla los gastos de operación")
        print("\nREGLAS:")
        print("- ACTIVO: Aumenta con DEBE, disminuye con HABER")
        print("- PASIVO/CAPITAL: Aumenta con HABER, disminuye con DEBE")
        print("- INGRESOS: Aumentan con HABER")
        print("- GASTOS: Aumentan con DEBE")
        print("="*50)
        input("\nPresiona Enter para continuar...")
    
    def gestionar_diario(self):
        while True:
            print("\n" + "="*40)
            print("           LIBRO DIARIO")
            print("="*40)
            print("1. 👀 Ver partidas existentes")
            print("2. ➕ Registrar nueva partida")
            print("3. ↩️ Volver al menú principal")
            print("="*40)
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                self.diario.mostrar_diario()
                input("\nPresiona Enter para continuar...")
            elif opcion == "2":
                self.registrar_nueva_partida()
            elif opcion == "3":
                break
            else:
                print("❌ Opción no válida.")
    
    def registrar_nueva_partida(self):
        try:
            print("\n➕ REGISTRAR NUEVA PARTIDA:")
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            descripcion = input("Descripción: ").strip()
            cuenta_debe = input("Cuenta Debe (ej: 1.1.1): ").strip()
            cuenta_haber = input("Cuenta Haber (ej: 4.1): ").strip()
            monto = float(input("Monto: $").strip())
            
            self.diario.registrar_partida(fecha, descripcion, cuenta_debe, cuenta_haber, monto)
            input("\nPresiona Enter para continuar...")
        except ValueError:
            print("❌ Error: El monto debe ser un número válido.")
        except Exception as e:
            print(f"❌ Error al registrar partida: {e}")
    
    def mostrar_mayor(self):
        print("\n📊 CARGANDO LIBRO MAYOR...")
        self.mayor.mostrar_mayor()
        input("\nPresiona Enter para continuar...")
    
    def crear_ajuste(self):
        try:
            print("\n🔧 CREAR PARTIDA DE AJUSTE:")
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            descripcion = input("Descripción del ajuste: ").strip()
            cuenta_debe = input("Cuenta Debe: ").strip()
            cuenta_haber = input("Cuenta Haber: ").strip()
            monto = float(input("Monto: $").strip())
            
            self.diario.crear_partida_ajuste(fecha, descripcion, cuenta_debe, cuenta_haber, monto)
            input("\nPresiona Enter para continuar...")
        except ValueError:
            print("❌ Error: El monto debe ser un número válido.")
        except Exception as e:
            print(f"❌ Error al crear ajuste: {e}")
    
    def mostrar_balanza(self):
        print("\n⚖️ GENERANDO BALANZA DE COMPROBACIÓN...")
        self.estados.balanza_comprobacion()
        input("\nPresiona Enter para continuar...")
    
    def mostrar_balance(self):
        print("\n💼 GENERANDO BALANCE GENERAL...")
        self.estados.balance_general()
        input("\nPresiona Enter para continuar...")
    
    def mostrar_estados_financieros(self):
        print("\n📈 GENERANDO ESTADOS FINANCIEROS COMPLETOS...")
        self.estados.balanza_comprobacion()
        self.estados.balance_general()
        input("\nPresiona Enter para continuar...")
    
    def crear_factura(self):
        try:
            print("\n🧾 CREAR FACTURA:")
            cliente = input("Nombre del cliente: ").strip()
            descripcion = input("Descripción del producto/servicio: ").strip()
            monto = float(input("Monto total: $").strip())
            
            self.facturacion.crear_factura(cliente, monto, descripcion)
            input("\nPresiona Enter para continuar...")
        except ValueError:
            print("❌ Error: El monto debe ser un número válido.")
        except Exception as e:
            print(f"❌ Error al crear factura: {e}")
    
    def mostrar_reporte_ventas(self):
        try:
            fecha = input("\n📊 Fecha para reporte (YYYY-MM-DD) o Enter para hoy: ").strip()
            if fecha == "":
                self.facturacion.reporte_ventas_diarias()
            else:
                self.facturacion.reporte_ventas_diarias(fecha)
            input("\nPresiona Enter para continuar...")
        except Exception as e:
            print(f"❌ Error al generar reporte: {e}")

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    try:
        print("🚀 INICIANDO SISTEMA CONTABLE...")
        sistema = SistemaContable()
        sistema.mostrar_menu()
    except KeyboardInterrupt:
        print("\n\n⏹️ Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")