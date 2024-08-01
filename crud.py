import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def buscar_cliente_por_id(cliente_id):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def actualizar_cliente(cliente_id, nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes SET nombre = ?, direccion = ?, telefono = ?, equipos = ?, ip = ?, velocidad = ?, fechaInstalacion = ?,
                   proximoPago = ?, mensualidad = ?, estado = ?, api = ?
        WHERE id = ?
    ''', (nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api, cliente_id))
    conn.commit()
    conn.close()

def eliminar_cliente(cliente_id):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()

def buscar_cliente():
    cliente_id = id_entry.get()
    cliente = buscar_cliente_por_id(cliente_id)

    if cliente:
        # Llenar los campos con los datos del cliente
        nombre_var.set(cliente[1])
        direccion_var.set(cliente[2])
        telefono_var.set(cliente[3])
        equipos_var.set(cliente[4])
        ip_var.set(cliente[5])
        velocidad_var.set(cliente[6])
        fechaInstalacion_var.set(cliente[7])
        proximoPago_var.set(cliente[8])
        mensualidad_var.set(cliente[9])
        estado_var.set(cliente[10])
        api_var.set(cliente[11])
        
        # Mostrar los campos de edición
        formulario_edicion.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    else:
        messagebox.showerror("Error", "Cliente no encontrado")

def guardar_cambios():
    cliente_id = id_entry.get()
    actualizar_cliente(cliente_id,
                       nombre_var.get(),
                       direccion_var.get(),
                       telefono_var.get(),
                       equipos_var.get(),
                       ip_var.get(),
                       velocidad_var.get(),
                       fechaInstalacion_var.get(),
                       proximoPago_var.get(),
                       mensualidad_var.get(),
                       estado_var.get(),
                       api_var.get())
    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")

def eliminar_cliente_action():
    cliente_id = id_entry.get()
    eliminar_cliente(cliente_id)
    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
    # Limpiar campos
    id_entry.delete(0, tk.END)
    formulario_edicion.grid_forget()

def ventana_buscar_cliente():
    global id_entry, nombre_var, direccion_var, telefono_var, equipos_var, ip_var, estado_var, proximoPago_var, velocidad_var, fechaInstalacion_var, mensualidad_var, api_var, formulario_edicion
    
    ventana = tk.Tk()
    ventana.title("Buscar Cliente")
    ventana.geometry("600x400")

    tk.Label(ventana, text="ID del Cliente:").grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(ventana, width=25)
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(ventana, text="Buscar", command=buscar_cliente).grid(row=0, column=2, padx=10, pady=10)

    # Variables para los campos de formulario
    nombre_var = tk.StringVar()
    direccion_var = tk.StringVar()
    telefono_var = tk.StringVar()
    equipos_var = tk.StringVar()
    ip_var = tk.StringVar()
    estado_var = tk.StringVar()
    proximoPago_var = tk.StringVar()
    velocidad_var = tk.StringVar()
    fechaInstalacion_var = tk.StringVar()
    mensualidad_var = tk.StringVar()
    api_var = tk.StringVar()

    # Formulario de edición
    formulario_edicion = tk.Frame(ventana)
    
    tk.Label(formulario_edicion, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=nombre_var, width=25).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Dirección").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=direccion_var, width=25).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Teléfono").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=telefono_var, width=25).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Equipos").grid(row=3, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=equipos_var, width=25).grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="IP").grid(row=4, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=ip_var, width=25).grid(row=4, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Velocidad").grid(row=5, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=velocidad_var, width=25).grid(row=5, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Fecha Instalación").grid(row=6, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=fechaInstalacion_var, width=25).grid(row=6, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Proximo Pago").grid(row=7, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=proximoPago_var, width=25).grid(row=7, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Mensualidad").grid(row=8, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=mensualidad_var, width=25).grid(row=8, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="Estado").grid(row=9, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=estado_var, width=25).grid(row=9, column=1, padx=10, pady=5)

    tk.Label(formulario_edicion, text="API").grid(row=10, column=0, padx=10, pady=5)
    tk.Entry(formulario_edicion, textvariable=api_var, width=25).grid(row=10, column=1, padx=10, pady=5)

    tk.Button(formulario_edicion, text="Guardar Cambios", command=guardar_cambios).grid(row=11, column=0, padx=10, pady=10)
    tk.Button(formulario_edicion, text="Eliminar Cliente", command=eliminar_cliente_action).grid(row=11, column=1, padx=10, pady=10)

    ventana.mainloop()

ventana_buscar_cliente()
