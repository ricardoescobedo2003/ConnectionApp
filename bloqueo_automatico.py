import sqlite3
import datetime
import paramiko
from tkinter import messagebox
import json 

def leer_credenciales():
    with open('credenciales.json', 'r') as archivo:
        datos = json.load(archivo)
        return datos

def gestionar_pagos_y_bloqueos():
    # Obtener la fecha actual y formatearla en un formato que entienda SQLite
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()

    # Obtener los pagos con fecha igual a la fecha actual
    cursor.execute('SELECT nombreCliente FROM pagos WHERE fechaPago = ?', (fecha_actual,))
    pagos_realizados = cursor.fetchall()
    pagos_realizados = [pago[0] for pago in pagos_realizados]

    # Obtener los clientes que no han realizado el pago
    cursor.execute('''
        SELECT nombre, ip FROM clientes 
        WHERE nombre NOT IN ({seq})
    '''.format(seq=','.join(['?']*len(pagos_realizados))), pagos_realizados)

    clientes_no_pagados = cursor.fetchall()

    # Datos para conexión SSH
    credenciales = leer_credenciales()
    hostname = credenciales['ip']
    username = credenciales['usuario']
    password = credenciales['password']

    new_speed = '0K/0K'  # Ancho de banda bloqueado

    # Función para bloquear cliente
    def bloquear_cliente(hostname, username, password, client_ip, new_speed):
        port = 22  # Puerto SSH, generalmente es 22
        command = f'/queue simple set [find target="{client_ip}/32"] max-limit={new_speed}'

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname, port, username, password)
            stdin, stdout, stderr = client.exec_command(command)
            
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if output:
                messagebox.showerror("Error", f"Output: {output}")
            if errors:
                messagebox.showerror("Error", f"Errors: {errors}")


        except Exception as e:
            print(f"Error: {e}")

        finally:
            client.close()

    # Bloquear a los clientes que no han pagado
    for cliente in clientes_no_pagados:
        nombre, ip = cliente
        bloquear_cliente(hostname, username, password, ip, new_speed)

        # Actualizar el estado del cliente a "suspendido"
        cursor.execute('UPDATE clientes SET estado = ? WHERE nombre = ?', ('suspendido', nombre))
        conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()
