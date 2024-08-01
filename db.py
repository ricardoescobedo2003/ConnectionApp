import sqlite3

# Función para crear la base de datos y las tablas
def crear_base_datos():
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    
    # Crear tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT NOT NULL,
            equipos TEXT NOT NULL,
            ip TEXT NOT NULL,
            velocidad TEXT NOT NULL,
            fechaInstalacion TEXT NOT NULL,
            proximoPago TEXT NOT NULL,
            mensualidad REAL NOT NULL,
            estado TEXT NOT NULL,
            api TEXT NOT NULL
        )
    ''')
    
    # Crear tabla pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreCliente TEXT NOT NULL,
            mensualidad REAL NOT NULL,
            fechaPago TEXT NOT NULL,
            proximoPago TEXT NOT NULL,
            FOREIGN KEY (nombreCliente) REFERENCES clientes(nombre)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Creacion de la base de datos con exito")
# Llamar a la función para crear la base de datos y las tablas
