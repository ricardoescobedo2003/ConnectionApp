import sqlite3

def registrar_cliente(nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion,
                   proximoPago, mensualidad, estado, api)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago,
          mensualidad, estado, api))
    conn.commit()
    conn.close()