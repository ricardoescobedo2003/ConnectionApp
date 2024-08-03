import sqlite3
import requests
import json
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import *

def leer_credenciales():
    with open('mensaje_automatico.json', 'r') as archivo:
        datos = json.load(archivo)
    return datos

def enviar_mensaje_automatico(phone_number, text, apikey):
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={text}&apikey={apikey}"
    response = requests.get(url)
    if response.status_code == 200:
        messagebox.showinfo("Envio exitoso", f"Mensaje enviado exitosamente a {phone_number}.")
    else:
        messagebox.showerror("Error al envio", f"Error al enviar el mensaje a {phone_number}: {response.status_code}")

def buscar_cliente_por_id(id_cliente):
    if not id_cliente:
        messagebox.showerror("Error", "Por favor, ingresa un ID de cliente.")
        return

    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, telefono, api FROM clientes WHERE id=?', (id_cliente,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        nombre_entry.delete(0, END)
        nombre_entry.insert(0, cliente[0])
        numero_entry.delete(0, END)
        numero_entry.insert(0, cliente[1])  # Corrección aquí
        api_entry.delete(0, END)
        api_entry.insert(0, cliente[2])  # Corrección aquí
    else:
        messagebox.showinfo("Información", "Cliente no encontrado.")

def datos_envio():
    phone_number = numero_entry.get()
    apikey = api_entry.get()
    text = ent_mensaje.get("1.0", "end-1c")  # Obtener texto del widget Text
    if phone_number and apikey and text:
        enviar_mensaje_automatico(phone_number, text, apikey)
    else:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos antes de enviar.")

def vista_mensaje_personal():
    tamano = 15

    vista_cambio_velocidad = tk.Tk()
    vista_cambio_velocidad.title("Mensaje Personalizado")
    vista_cambio_velocidad.geometry("750x350")
    vista_cambio_velocidad.resizable(False, False)

    global id_entry, nombre_entry, numero_entry, api_entry, ent_mensaje

    id_label = tk.Label(vista_cambio_velocidad, text="Id del Cliente")
    id_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    buscar_button = tk.Button(vista_cambio_velocidad, text="Buscar", width=20, command=lambda: buscar_cliente_por_id(id_entry.get()))

    nombre_label = tk.Label(vista_cambio_velocidad, text="Nombre Cliente")
    nombre_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    numero_label = tk.Label(vista_cambio_velocidad, text="Número")
    numero_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    api_label = tk.Label(vista_cambio_velocidad, text="API")
    api_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    lb_mensaje = tk.Label(vista_cambio_velocidad, text="Mensaje")
    ent_mensaje = tk.Text(vista_cambio_velocidad, height=5, width=40)  # Ajustado el tamaño del widget Text

    # Layout usando grid
    id_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    buscar_button.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky='ew')

    nombre_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    nombre_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky='ew')

    numero_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    numero_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky='ew')

    api_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    api_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2, sticky='ew')

    lb_mensaje.grid(row=4, column=0, padx=10, pady=10, sticky='w')
    ent_mensaje.grid(row=4, column=1, padx=10, pady=10, columnspan=3, sticky='nsew')

    # Configurar el grid para expandirse
    vista_cambio_velocidad.grid_columnconfigure(1, weight=1)
    vista_cambio_velocidad.grid_rowconfigure(4, weight=1)

    # Crear un Frame para agrupar los botones
    frame_botones = tk.Frame(vista_cambio_velocidad)
    frame_botones.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

    # Botón Enviar
    enviar_button = tk.Button(frame_botones, text="Enviar Mensaje", width=25, command=datos_envio)
    enviar_button.pack(side=tk.LEFT, padx=5)

    # Botón Cancelar
    cancelar_button = tk.Button(frame_botones, text="Cancelar", width=25, command=vista_cambio_velocidad.destroy)
    cancelar_button.pack(side=tk.LEFT, padx=5)

    vista_cambio_velocidad.mainloop()
