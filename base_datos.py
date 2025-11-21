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

        # Tabla para menú del restaurante
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_restaurante (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                descripcion TEXT
            )
        ''')

        # Insertar menú base si está vacío
        cursor.execute('SELECT COUNT(*) FROM menu_restaurante')
        if cursor.fetchone()[0] == 0:
            menu_base = [
                ('Risotto de Champiñones', 'Plato Principal', 25.99, 'Risotto cremoso con champiñones frescos y parmesano'),
                ('Salmón a la Parrilla', 'Plato Principal', 32.99, 'Salmón fresco con verduras de temporada'),
                ('Pasta Carbonara', 'Plato Principal', 22.99, 'Pasta tradicional italiana con panceta y huevo'),
                ('Ensalada César', 'Entrada', 15.99, 'Ensalada fresca con aderezo César casero'),
                ('Tiramisú', 'Postre', 12.99, 'Postre italiano clásico con café y mascarpone'),
                ('Vino Tinto Reserva', 'Bebida', 18.99, 'Vino tinto de la mejor cosecha'),
                ('Café Espresso', 'Bebida', 4.99, 'Café italiano auténtico'),
                ('Agua Mineral', 'Bebida', 3.99, 'Agua mineral natural')
            ]
            cursor.executemany('INSERT INTO menu_restaurante (nombre, categoria, precio, descripcion) VALUES (?, ?, ?, ?)', menu_base)

        # Tabla para productos en factura (detalle de pedidos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos_factura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                producto_id INTEGER,
                nombre_producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (factura_id) REFERENCES facturas (id)
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
    