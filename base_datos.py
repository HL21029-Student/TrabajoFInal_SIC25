import sqlite3
import os

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
    