from base_datos import BaseDatos
from datetime import datetime

class Facturacion:
    def __init__(self):
        self.db = BaseDatos()

    def mostrar_menu_restaurante(self):
        menu = self.db.obtener_datos('SELECT * FROM menu_restaurante ORDER BY categoria, nombre')
        print("\n--- MENÚ DEL RESTAURANTE ---")
        categorias = {}
        for item in menu:
            cat = item[2]
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(item)

        for categoria, items in categorias.items():
            print(f"\n{categoria.upper()}:")
            for item in items:
                print(f"  {item[0]}. {item[1]} - ${item[3]:.2f} ({item[4]})")
        return menu

    def crear_factura(self, cliente, items=None, total=None):
        if items is None:
            items = []
            print("\n--- CREANDO PEDIDO ---")
            menu = self.mostrar_menu_restaurante()
            while True:
                try:
                    id_item = input("ID del plato/bebida (o 'fin' para terminar): ")
                    if id_item.lower() == 'fin':
                        break
                    id_item = int(id_item)
                    item = next((i for i in menu if i[0] == id_item), None)
                    if not item:
                        print("ID no válido.")
                        continue
                    cantidad = int(input(f"Cantidad de {item[1]}: "))
                    precio_unitario = item[3]
                    subtotal = cantidad * precio_unitario
                    items.append({
                        'producto_id': item[0],
                        'nombre_producto': item[1],
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'subtotal': subtotal
                    })
                    print(f"Agregado: {cantidad} x {item[1]} = ${subtotal:.2f}")
                except ValueError:
                    print("Entrada no válida.")

        if not items:
            print("No se agregaron items.")
            return None

        total = sum(item['subtotal'] for item in items)
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.ejecutar_consulta(
            'INSERT INTO facturas (fecha, cliente, monto, descripcion) VALUES (?, ?, ?, ?)',
            (fecha, cliente, total, f"Pedido para {cliente}")
        )
        factura_id = self.db.obtener_datos('SELECT last_insert_rowid()')[0][0]

        for item in items:
            self.db.ejecutar_consulta(
                'INSERT INTO productos_factura (factura_id, producto_id, nombre_producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)',
                (factura_id, item['producto_id'], item['nombre_producto'], item['cantidad'], item['precio_unitario'], item['subtotal'])
            )

        return factura_id

    def mostrar_factura(self, factura_id):
        factura = self.db.obtener_datos(
            'SELECT * FROM facturas WHERE id = ?',
            (factura_id,)
        )[0]

        detalles = self.db.obtener_datos(
            'SELECT * FROM productos_factura WHERE factura_id = ?',
            (factura_id,)
        )

        print(f"\n--- FACTURA #{factura[0]} ---")
        print(f"Cliente: {factura[2]}")
        print(f"Fecha: {factura[1]}")
        print(f"Total: ${factura[3]:.2f}")
        print(f"Descripción: {factura[4]}")
        print("\nDetalles del Pedido:")
        for detalle in detalles:
            print(f"- {detalle[3]} x {detalle[4]} = ${detalle[6]:.2f}")
        print(f"\nTotal: ${factura[3]:.2f}")

    def listar_facturas(self):
        facturas = self.db.obtener_datos('SELECT * FROM facturas ORDER BY fecha DESC')
        print("\n--- LISTADO DE FACTURAS ---")
        for factura in facturas:
            print(f"#{factura[0]} - {factura[2]} - {factura[1]} - ${factura[3]:.2f}")
        return facturas

    def generar_reporte_ventas_diarias(self):
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        ventas = self.db.obtener_datos(
            "SELECT * FROM facturas WHERE date(fecha) = ?",
            (fecha_hoy,)
        )
        
        total_ventas = 0
        print(f"\n--- REPORTE DE VENTAS DIARIAS ({fecha_hoy}) ---")
        for venta in ventas:
            print(f"#{venta[0]} - {venta[2]} - {venta[1]} - ${venta[3]:.2f}")
            total_ventas += venta[3]
        
        print(f"\nTotal de Ventas de Hoy: ${total_ventas:.2f}")

    def exportar_factura_txt(self, factura_id):
        factura = self.db.obtener_datos('SELECT * FROM facturas WHERE id = ?', (factura_id,))[0]
        detalles = self.db.obtener_datos('SELECT * FROM productos_factura WHERE factura_id = ?', (factura_id,))
        
        nombre_archivo = f"factura_{factura_id}.txt"
        with open(nombre_archivo, 'w') as f:
            f.write(f"--- FACTURA #{factura[0]} ---\n")
            f.write(f"Cliente: {factura[2]}\n")
            f.write(f"Fecha: {factura[1]}\n")
            f.write(f"Total: ${factura[3]:.2f}\n")
            f.write(f"Descripción: {factura[4]}\n")
            f.write("\nDetalles del Pedido:\n")
            for detalle in detalles:
                f.write(f"- {detalle[3]} x {detalle[4]} = ${detalle[6]:.2f}\n")
            f.write(f"\nTotal: ${factura[3]:.2f}\n")
        
        print(f"Factura exportada a {nombre_archivo}")
