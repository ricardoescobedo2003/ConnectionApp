import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

def leer_usuarios(filtro=None):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    
    query = 'SELECT id, nombreCliente, mensualidad, fechaPago, proximoPago FROM pagos'
    
    if filtro:
        if filtro['type'] == 'recent':
            query += ' ORDER BY fechaPago DESC'
        elif filtro['type'] == 'name':
            query += ' WHERE nombreCliente LIKE ?'
        elif filtro['type'] == 'month_year':
            query += ' WHERE strftime("%Y-%m", fechaPago) = ?'
    
    cursor.execute(query, filtro['params'] if filtro else ())
    pagos = cursor.fetchall()
    conn.close()
    return pagos

def aplicar_filtro(filtro_var, entry_nombre, entry_mes_anio):
    tipo_filtro = filtro_var.get()
    
    if tipo_filtro == 'recent':
        filtro = {'type': 'recent'}
    elif tipo_filtro == 'name':
        nombre = entry_nombre.get()
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre para buscar.")
            return
        filtro = {'type': 'name', 'params': (f"%{nombre}%",)}
    elif tipo_filtro == 'month_year':
        mes_anio = entry_mes_anio.get()
        try:
            datetime.strptime(mes_anio, "%Y-%m")
        except ValueError:
            messagebox.showwarning("Advertencia", "El formato de mes y año debe ser YYYY-MM.")
            return
        filtro = {'type': 'month_year', 'params': (mes_anio,)}
    else:
        filtro = None
    
    mostrar_datos(filtro=filtro, filtro_var=filtro_var, entry_nombre=entry_nombre, entry_mes_anio=entry_mes_anio)

def mostrar_datos(filtro=None, filtro_var=None, entry_nombre=None, entry_mes_anio=None):
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Pagos Registrados")
    ventana.geometry("900x600")
    ventana.resizable(False, False)
    
    # Crear Treeview
    tree = ttk.Treeview(ventana, columns=("Id", "Nombre", "Mensualidad", "Fecha_de_Pago", "Proximo_Pago"), show="headings")
    
    # Definir las columnas
    tree.heading("Id", text="Id")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Mensualidad", text="Mensualidad")
    tree.heading("Fecha_de_Pago", text="Fecha de Pago")
    tree.heading("Proximo_Pago", text="Siguiente Pago")
    
    # Definir el ancho de las columnas
    tree.column("Nombre", width=150)
    tree.column("Mensualidad", width=150)
    tree.column("Fecha_de_Pago", width=100)
    tree.column("Proximo_Pago", width=100)
    
    # Insertar datos en la tabla
    for item in tree.get_children():
        tree.delete(item)
    
    pagos = leer_usuarios(filtro)
    for pago in pagos:
        tree.insert("", tk.END, values=pago)
    
    tree.pack(expand=True, fill="both")
    
    # Crear campos de filtro
    filtro_frame = tk.Frame(ventana)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por:").grid(row=0, column=0, padx=5)

    filtro_var = tk.StringVar(value="recent")
    tk.Radiobutton(filtro_frame, text="Más reciente", variable=filtro_var, value="recent").grid(row=0, column=1, padx=5)
    tk.Radiobutton(filtro_frame, text="Nombre", variable=filtro_var, value="name").grid(row=0, column=2, padx=5)
    tk.Radiobutton(filtro_frame, text="Mes/Año", variable=filtro_var, value="month_year").grid(row=0, column=3, padx=5)



    entry_nombre = tk.Entry(filtro_frame)
    entry_nombre.grid(row=1, column=2, padx=5, pady=5)
    
    entry_mes_anio = tk.Entry(filtro_frame)
    entry_mes_anio.grid(row=1, column=3, padx=5, pady=5)
    
    tk.Button(filtro_frame, text="Aplicar Filtro", command=lambda: aplicar_filtro(filtro_var, entry_nombre, entry_mes_anio)).grid(row=1, column=4, padx=5, pady=5)

    ventana.mainloop()

