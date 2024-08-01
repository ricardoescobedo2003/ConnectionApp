import paramiko
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
import json



def buscar_cliente_por_id(id_cliente):
    cliente_id = id_cliente
    if not cliente_id:
        messagebox.showerror("Error", "Por favor, ingresa un ID de cliente.")
        return

    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api FROM clientes WHERE id=?', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        nombre_entry.delete(0, END)
        nombre_entry.insert(0, cliente[0])
        ip_entry.delete(0, END)
        ip_entry.insert(0, cliente[4])
        velocidad_entry.delete(0, END)
        velocidad_entry.insert(0, cliente[5])


    else:
        messagebox.showinfo("Información", "Cliente no encontrado.")


def ventana_cambio_velocidad():

    def obtener_datos():
        id_cliente = id_entry.get()
        buscar_cliente_por_id(id_cliente)

    global id_entry, nombre_entry, ip_entry, velocidad_entry

    def leer_credenciales():
        with open('credenciales.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos
            

    def change_client_speed_mikrotik(hostname, username, password, client_ip, new_speed):

        port = 22  # Puerto SSH, generalmente es 22

        # Comando para ajustar el ancho de banda
        command = f'/queue simple set [find target="{client_ip}/32"] max-limit={new_speed}'

        # Crear una instancia del cliente SSH
        client = paramiko.SSHClient()

        # Agregar automáticamente la clave del servidor si no está en la lista de known hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Conectarse al dispositivo
            client.connect(hostname, port, username, password)
            
            # Ejecutar el comando para ajustar el ancho de banda
            stdin, stdout, stderr = client.exec_command(command)
            
            # Leer y mostrar la salida del comando, si es necesario
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if output:
                messagebox.showerror("Error", f"Output: {output}")
            if errors:
                messagebox.showerror("Error", f"Errors: {errors}")

            messagebox.showinfo("Cambio exitoso", f"La velocidad del cliente {client_ip} ha sido cambiada a {new_speed}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Cerrar la conexión
            client.close()


# Llamar a la función


    def funcion_perrona_de_velocidad():

        credenciales = leer_credenciales()
        hostname = credenciales['ip']
        username = credenciales['usuario']
        password = credenciales['password']

        port = 22  # Ajusta el puerto si es necesario
        client_ip = ip_entry.get()
        velocidad_subida = velocidad_entry_nueva.get()
        velocidad_bajada = bajada_velocidad_entry_nueva.get()
        medicion_subida = opciones.get()
        medicion_bajada = bajada_opciones.get()
        new_speed = velocidad_subida + medicion_subida + "/" + velocidad_bajada + medicion_bajada
        change_client_speed_mikrotik(hostname, username, password, client_ip, new_speed)

    tamano = 20

    valores = ["M", "k"]

    vista_cambio_velocidad = tk.Tk()
    vista_cambio_velocidad.title("Cambio de velocidad")
    vista_cambio_velocidad.geometry("750x350")
    vista_cambio_velocidad.resizable(False, False)

    id_label = tk.Label(vista_cambio_velocidad, text="Id del Cliente")
    id_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    buscar_button = tk.Button(vista_cambio_velocidad, text="Buscar", width=20, command=obtener_datos)

    nombre_label = tk.Label(vista_cambio_velocidad, text="Nombre Cliente")
    nombre_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    ip_label = tk.Label(vista_cambio_velocidad, text="Ip Cliente")
    ip_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    velocidad_label = tk.Label(vista_cambio_velocidad, text="Velocidad Actual")
    velocidad_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    lb_velocidad_nueva = Label(vista_cambio_velocidad, text="Velocidad Nueva")
    velocidad_entry_nueva = Entry(vista_cambio_velocidad, width=tamano)
    opciones = ttk.Combobox(vista_cambio_velocidad, values=valores)
    lb_mediciones = Label(vista_cambio_velocidad, text="/s Subida")

    bajada_lb_velocidad_nueva = Label(vista_cambio_velocidad, text="Velocidad Nueva")
    bajada_velocidad_entry_nueva = Entry(vista_cambio_velocidad, width=tamano)
    bajada_opciones = ttk.Combobox(vista_cambio_velocidad, values=valores)
    bajada_lb_mediciones = Label(vista_cambio_velocidad, text="/s Bajada")

    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    buscar_button.grid(row=0, column=2, padx=10, pady=10)

    nombre_label.grid(row=2, column=0, padx=10, pady=10)
    nombre_entry.grid(row=2, column=1, padx=10, pady=10)

    ip_label.grid(row=2, column=2, padx=10, pady=10)
    ip_entry.grid(row=2, column=3, padx=10, pady=10)    

    velocidad_label.grid(row=3, column=0, padx=10, pady=10)
    velocidad_entry.grid(row=3, column=1, padx=10, pady=10)

    lb_velocidad_nueva.grid(row=5, column=0, padx=10, pady=10)
    velocidad_entry_nueva.grid(row=5, column=1, padx=10, pady=10)
    opciones.grid(row=5, column=2, padx=10, pady=10)
    lb_mediciones.grid(row=5, column=3, padx=10, pady=10)

    bajada_lb_velocidad_nueva.grid(row=6, column=0, padx=10, pady=10)
    bajada_velocidad_entry_nueva.grid(row=6, column=1, padx=10, pady=10)
    bajada_opciones.grid(row=6, column=2, padx=10, pady=10)
    bajada_lb_mediciones.grid(row=6, column=3, padx=10, pady=10)

    # Añadir un separador horizontal
    separador = ttk.Separator(vista_cambio_velocidad, orient='horizontal')
    separador.grid(row=1, column=0, columnspan=5, sticky='ew', padx=10, pady=10)

    separador_dos = ttk.Separator(vista_cambio_velocidad, orient='horizontal')
    separador_dos.grid(row=4, column=0, columnspan=5, sticky='ew', padx=10, pady=10)

    # Crear un Frame para agrupar los botones
    frame_botones = tk.Frame(vista_cambio_velocidad)
    frame_botones.grid(column=0, row=7, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = tk.Button(frame_botones, text="Cambiar Velocidad", width=25, command=funcion_perrona_de_velocidad)
    guardar.pack(side=tk.LEFT, padx=5)

    # Botón Cancelar
    cancela = tk.Button(frame_botones, text="Cancelar", width=25, command=vista_cambio_velocidad.destroy)
    cancela.pack(side=tk.LEFT, padx=5)

    vista_cambio_velocidad.mainloop()
