import os
import json
from PIL import Image, ImageTk
from db import crear_base_datos
from tkinter import Menu, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox
from tkinter import ttk
from vista_cliente_registro import ventana_principal_registro
from mostrar_tabla_clientes import mostrar_datos_cliente
from editar_buscar_eliminar import ventana_buscar_actualizar
import webbrowser
from registrar_pago_vista import ventana_buscar_cliente_pagar
from ver_pagos_tabla import mostrar_datos
from vista_credenciales_microtik import vista_credenciales
from cambio_de_velocidad import ventana_cambio_velocidad
from bloqueos_desbloqueo import vista_bloqueo_desbloque
from bloqueo_automatico import gestionar_pagos_y_bloqueos
import tkinter as tk
import sqlite3
from name_wisp import nombre_wisp
from reiniciar_antena import reiniciar
from definir_mensaje_automatico import definir_mensaje_automatico
from enviar_mensaje_automatoco_vs import iniciar_envio_masivo_automatico
from enviar_mensaje_personal import vista_mensaje_personal

valid_keys = ['NhqnMHGR074PjBPG', 'anotherkey789012', 'MinuzaFea265/']

url = "https://www.facebook.com/profile.php?id=100065750894627"


crear_base_datos()

def verify_activation_key(input_key):
    return input_key in valid_keys

def check_activation():
    user_key = activation_key.get()
    if verify_activation_key(user_key):
        messagebox.showinfo("Activacion", "Activacion satisfactoria!")
        store_activation_key(user_key)
        activation_window.destroy()
        create_main_window()
    else:
        messagebox.showerror("Activation", "Invalid activation key. Please try again.")

def store_activation_key(key):
    config = {'activation_key': key}
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def load_activation_key():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get('activation_key')
    return None






# Lista de velocidades
velocidades = ["100M/10", "100M15M", "100M/20M", "100M/25M", "100M/30M", "100M/50M",
               "100M/60M", "100M/70M", "100M/80M", "100M/90M", "100M/100M",
               "200M/200M", "250M/250M", "300M/300M", "Seleccion Libre"]

# Función para leer usuarios
def leer_usuarios(nombre="", ip="", velocidad="", mensualidad=""):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    query = 'SELECT id, nombre, direccion, telefono, api, ip, estado, proximoPago FROM clientes WHERE 1=1'
    
    params = []
    if nombre:
        query += ' AND nombre LIKE ?'
        params.append(f'%{nombre}%')
    if ip:
        query += ' AND ip LIKE ?'
        params.append(f'%{ip}%')
    if velocidad:
        query += ' AND velocidad LIKE ?'
        params.append(f'%{velocidad}%')
    if mensualidad:
        query += ' AND mensualidad LIKE ?'
        params.append(f'%{mensualidad}%')
    
    cursor.execute(query, params)
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Función para aplicar filtro
def aplicar_filtro():
    nombre = entry_nombre.get()
    ip = entry_ip.get()
    velocidad = entry_velocidad.get()
    mensualidad = entry_mensualidad.get()
    
    # Limpiar la tabla actual
    for item in tree.get_children():
        tree.delete(item)
    
    # Obtener datos filtrados y actualizar la tabla
    usuarios = leer_usuarios(nombre, ip, velocidad, mensualidad)
    for usuario in usuarios:
        # Insertar datos en la tabla
        item_id = tree.insert("", tk.END, values=usuario)
        
        # Colorear la fila en función del estado
        estado = usuario[6]  # Suponiendo que 'estado' está en la posición 6
        if estado == "activado":
            tree.item(item_id, tags=("activado",))
        elif estado == "suspendido":
            tree.item(item_id, tags=("suspendido",))
        elif estado == "desactivado":
            tree.item(item_id, tags=("desactivado",))

# Función para crear la ventana principal
def create_main_window():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Connection")
    root.geometry("900x600")
    root.resizable(False, False)

    # Crear la barra de menú
    menu_bar = Menu(root)

    # Crear el menú Cliente
    cliente_menu = Menu(menu_bar, tearoff=0)
    cliente_menu.add_command(label="Crear Cliente", command=crear_cliente)
    cliente_menu.add_command(label="Ver Cliente", command=ver_cliente)
    cliente_menu.add_command(label="Buscar Cliente", command=buscar_cliente)
    menu_bar.add_cascade(label="Cliente", menu=cliente_menu)

    # Crear el menú Pagos
    pagos_menu = Menu(menu_bar, tearoff=0)
    pagos_menu.add_command(label="Registrar Pago", command=registrar_pago)
    pagos_menu.add_command(label="Ver Pagos", command=ver_pagos)
    menu_bar.add_cascade(label="Pagos", menu=pagos_menu)

    # Crear el menú Herramientas de red
    herramientas_red_menu = Menu(menu_bar, tearoff=0)
    herramientas_red_menu.add_command(label="Credenciales Microtik", command=credenciales_microtik)
    herramientas_red_menu.add_command(label="Cambio Velocidad", command=ventana_cambio_velocidad)
    herramientas_red_menu.add_command(label="Desbloquear/Bloquear Cliente", command=desbloquear_cliente)
    herramientas_red_menu.add_command(label="Cortes Automáticos", command=cortes_automaticos)
    menu_bar.add_cascade(label="Herramientas de red", menu=herramientas_red_menu)


    
    herramientas_ubiquiti = Menu(menu_bar, tearoff=0)
    herramientas_ubiquiti.add_command(label="Reiniciar antena", command=reiniciar)
    herramientas_ubiquiti.add_command(label="Cambio Velocidad", command=proximamente)
    herramientas_ubiquiti.add_command(label="Informacion", command=proximamente)
    menu_bar.add_cascade(label="Herramientas Ubiquiti", menu=herramientas_ubiquiti)

    # Crear el menú Herramientas de red
    opciones_wisp = Menu(menu_bar, tearoff=0)
    opciones_wisp.add_command(label="Nombre de wisp", command=nombre_wisp)
    menu_bar.add_cascade(label="Opciones de wisp", menu=opciones_wisp)


    # Crear el menú Herramientas de red
    opciones_bot = Menu(menu_bar, tearoff=0)
    opciones_bot.add_command(label="Definir mensaje automatico", command=definir_mensaje_automatico)
    opciones_bot.add_command(label="Enviar mensaje automatico", command=iniciar_envio_masivo_automatico)
    opciones_bot.add_command(label="Enviar mensaje personalizado", command=vista_mensaje_personal)
    menu_bar.add_cascade(label="BotWhatsApp", menu=opciones_bot)

    # Crear opción de creación de base
    creacion_base = Menu(menu_bar, tearoff=0)
    creacion_base.add_command(label="?", command=version)
    creacion_base.add_command(label="Contacto", command=acerca_de)
    creacion_base.add_command(label="Salir", command=root.destroy)
    menu_bar.add_cascade(label="Información", menu=creacion_base)

    # Mostrar la barra de menú
    root.config(menu=menu_bar)

    # Crear marco para filtros
    marco_filtros = tk.Frame(root)
    marco_filtros.pack(pady=10)

    # Campos de filtro
    tk.Label(marco_filtros, text="Nombre:").grid(row=0, column=0, padx=5)
    global entry_nombre
    entry_nombre = tk.Entry(marco_filtros)
    entry_nombre.grid(row=0, column=1, padx=5)

    tk.Label(marco_filtros, text="IP:").grid(row=1, column=0, padx=5)
    global entry_ip
    entry_ip = tk.Entry(marco_filtros)
    entry_ip.grid(row=1, column=1, padx=5)

    tk.Label(marco_filtros, text="Velocidad:").grid(row=2, column=0, padx=5)
    global entry_velocidad
    entry_velocidad = ttk.Combobox(marco_filtros, values=velocidades)
    entry_velocidad.grid(row=2, column=1, padx=5)

    tk.Label(marco_filtros, text="Mensualidad:").grid(row=3, column=0, padx=5)
    global entry_mensualidad
    entry_mensualidad = tk.Entry(marco_filtros)
    entry_mensualidad.grid(row=3, column=1, padx=5)

    # Botón para aplicar filtro
    boton_filtro = tk.Button(marco_filtros, text="Aplicar Filtro", command=aplicar_filtro)
    boton_filtro.grid(row=4, columnspan=2, pady=10)

    # Crear Treeview
    global tree
    tree = ttk.Treeview(root, columns=("Id", "Nombre", "Direccion", "Telefono", "api", "IP", "Estado", "ProximoPago"), show="headings")
    
    # Definir las columnas
    tree.heading("Id", text="Id")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Direccion", text="Direccion")
    tree.heading("Telefono", text="Telefono")
    tree.heading("api", text="api")
    tree.heading("IP", text="IP")
    tree.heading("Estado", text="Estado")
    tree.heading("ProximoPago", text="Proximo Pago")
    
    # Definir el ancho de las columnas
    tree.column("Nombre", width=150)
    tree.column("Direccion", width=150)
    tree.column("Telefono", width=100)
    tree.column("api", width=100)
    tree.column("IP", width=100)
    tree.column("Estado", width=100)
    tree.column("ProximoPago", width=150)

    # Configurar las etiquetas de estilo
    tree.tag_configure("activado", background="lightgreen")
    tree.tag_configure("suspendido", background="lightcoral")
    tree.tag_configure("desactivado", background="lightgray")
    
    # Crear menú contextual
    menu_contextual = Menu(root, tearoff=0)
    menu_contextual.add_command(label="Actualizar", command=aplicar_filtro)

    def mostrar_menu_contextual(event):
        menu_contextual.post(event.x_root, event.y_root)

    # Asociar el menú contextual al Treeview
    tree.bind("<Button-3>", mostrar_menu_contextual)
    
    tree.pack(expand=True, fill="both")
    # Insertar datos iniciales en la tabla
    aplicar_filtro()
    
    tree.pack(expand=True, fill="both")

    root.mainloop()

def crear_cliente():
    ventana_principal_registro()
    
def ver_cliente():
    mostrar_datos_cliente()

def buscar_cliente():
    ventana_buscar_actualizar()

def registrar_pago():
    ventana_buscar_cliente_pagar()

def ver_pagos():
    mostrar_datos()

def credenciales_microtik():
    vista_credenciales()

def bloquear_cliente():
    vista_bloqueo_desbloque()

def cortes_automaticos():
    valor = messagebox.askyesno("Iniciar", "Deseas iniciar los cortes automatico?")
    if valor == True:
        gestionar_pagos_y_bloqueos
    else:
        messagebox.showinfo("Cancelado", "No se realizara ningun corte automatico")
        
def desbloquear_cliente():
    vista_bloqueo_desbloque()

def proximamente():
    messagebox.showinfo("Proximamente", "Aun encontramos trabajando con estas opciones. En la proxima version Connectio v1.0")

def acerca_de():
    webbrowser.open(url)

def version():
    messagebox.askyesno("Informacion", "Software Connection para wisp desarrollado por Ing Escobedo. Con la version 0.9")   
    
# Verificar si ya hay una clave de activación almacenada
stored_key = load_activation_key()

if stored_key and verify_activation_key(stored_key):
    print('Activation already verified.')
    create_main_window()

else:
    # Crear la ventana de activación
    activation_window = Tk()
    activation_window.title("Activacion")
    activation_window.geometry("300x150")
    activation_window.resizable(False, False)

    # Establecer el icono de la ventana de activación

    activation_key = StringVar()

    Label(activation_window, text="Ingresa la llave de activacion:").pack(pady=10)
    Entry(activation_window, textvariable=activation_key).pack(pady=5)
    Button(activation_window, text="Activar", command=check_activation).pack(pady=10)

    activation_window.mainloop()
