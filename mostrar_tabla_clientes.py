import tkinter as tk
from tkinter import ttk
import sqlite3



velocidades = ["100M/10", "100M15M", "100M/20M", "100M/25M", "100M/30M", "100M/50M",
               "100M/60M", "100M/70M", "100M/80M", "100M/90M", "100M/100M",
               "200M/200M", "250M/250M", "300M/300M", "Seleccion Libre"]




def leer_usuarios(nombre="", ip="", velocidad="", mensualidad=""):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    query = 'SELECT id, nombre, direccion, telefono, equipos, ip, estado, proximoPago FROM clientes WHERE 1=1'
    
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

def mostrar_datos_cliente():
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Clientes Registrados")
    ventana.geometry("900x600")
    ventana.resizable(False, False)

    # Crear marco para filtros
    marco_filtros = tk.Frame(ventana)
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
    tree = ttk.Treeview(ventana, columns=("Id", "Nombre", "Direccion", "Telefono", "Equipos", "IP", "Estado", "ProximoPago"), show="headings")
    
    # Definir las columnas
    tree.heading("Id", text="Id")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Direccion", text="Direccion")
    tree.heading("Telefono", text="Telefono")
    tree.heading("Equipos", text="Equipos")
    tree.heading("IP", text="IP")
    tree.heading("Estado", text="Estado")
    tree.heading("ProximoPago", text="Proximo Pago")
    
    # Definir el ancho de las columnas
    tree.column("Nombre", width=150)
    tree.column("Direccion", width=150)
    tree.column("Telefono", width=100)
    tree.column("Equipos", width=100)
    tree.column("IP", width=100)
    tree.column("Estado", width=100)
    tree.column("ProximoPago", width=150)

    # Configurar las etiquetas de estilo
    tree.tag_configure("activado", background="lightgreen")
    tree.tag_configure("suspendido", background="lightcoral")
    tree.tag_configure("desactivado", background="lightgray")

    # Insertar datos iniciales en la tabla
    aplicar_filtro()
    
    tree.pack(expand=True, fill="both")

    ventana.mainloop()

