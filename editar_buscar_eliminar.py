import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Función para buscar cliente por ID y rellenar los widgets Entry
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
        nombre_entry.delete(0, tk.END)
        nombre_entry.insert(0, cliente[0])
        direccion_entry.delete(0, tk.END)
        direccion_entry.insert(0, cliente[1])
        telefono_entry.delete(0, tk.END)
        telefono_entry.insert(0, cliente[2])
        equipos_entry.delete(0, tk.END)
        equipos_entry.insert(0, cliente[3])
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, cliente[4])
        velocidad_entry.delete(0, tk.END)
        velocidad_entry.insert(0, cliente[5])

        mensualidad_entry.delete(0, tk.END)
        mensualidad_entry.insert(0, cliente[8])

    else:
        messagebox.showinfo("Información", "Cliente no encontrado.")

# Función para actualizar el cliente
def actualizar_cliente_gui():
    cliente_id = id_entry.get()
    nombre = nombre_entry.get()
    direccion = direccion_entry.get()
    telefono = telefono_entry.get()
    equipos = equipos_entry.get()
    ip = ip_entry.get()
    velocidad = velocidad_entry.get()
    mensualidad = mensualidad_entry.get()

    if not cliente_id:
        messagebox.showerror("Error", "El ID del cliente es necesario para actualizar.")
        return

    actualizar_cliente(cliente_id, nombre, direccion, telefono, equipos, ip, velocidad, mensualidad)
    messagebox.showinfo("Información", "Cliente actualizado correctamente.")

def actualizar_cliente(cliente_id, nombre, direccion, telefono, equipos, ip, velocidad, mensualidad):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes SET nombre = ?, direccion = ?, telefono = ?, equipos = ?, ip = ?, velocidad = ?,
                   mensualidad = ?
        WHERE id = ?
    ''', (nombre, direccion, telefono, equipos, ip, velocidad, mensualidad, cliente_id))
    conn.commit()
    conn.close()


def eliminar_cliente(cliente_id):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Eliminado", "Cliente eliminado de manera correcta")


def ventana_buscar_actualizar():
    def obtener_datos():
        id_cliente = id_entry.get()        
        buscar_cliente_por_id(id_cliente)

    def eliminar_datos():
        cliente_id = id_entry.get()
        eliminar_cliente(cliente_id)


    global id_entry, nombre_entry, direccion_entry, telefono_entry, equipos_entry, ip_entry, velocidad_entry, fecha_instalacion_entry, proximo_pago_entry, mensualidad_entry, estado_entry, api_entry

    vistaRegistro = tk.Tk()
    vistaRegistro.title("Actualizar & Eliminar")
    vistaRegistro.geometry("750x300")
    vistaRegistro.resizable(False, False)

    id_label = tk.Label(vistaRegistro, text="Id del Cliente")
    id_entry = tk.Entry(vistaRegistro, width=25)

    buscar_button = tk.Button(vistaRegistro, text="Buscar", width=20, command=obtener_datos)

    nombre_label = tk.Label(vistaRegistro, text="Nombre Cliente")
    nombre_entry = tk.Entry(vistaRegistro, width=25)

    direccion_label = tk.Label(vistaRegistro, text="Direccion")
    direccion_entry = tk.Entry(vistaRegistro, width=25)

    telefono_label = tk.Label(vistaRegistro, text="Telefono")
    telefono_entry = tk.Entry(vistaRegistro, width=25)

    equipos_label = tk.Label(vistaRegistro, text="Equipos")
    equipos_entry = tk.Entry(vistaRegistro, width=25)

    ip_label = tk.Label(vistaRegistro, text="Ip Cliente")
    ip_entry = tk.Entry(vistaRegistro, width=25)

    velocidad_label = tk.Label(vistaRegistro, text="Velocidad")
    velocidad_entry = tk.Entry(vistaRegistro, width=25)


    mensualidad_label = tk.Label(vistaRegistro, text="Mensualidad")
    mensualidad_entry = tk.Entry(vistaRegistro, width=25)

    api_label = tk.Label (vistaRegistro, text="ApI")
    ent_api = tk.Entry(vistaRegistro, width=25)

    id_label.grid(column=0, row=0, padx=10, pady=10)
    id_entry.grid(column=1, row=0, padx=10, pady=10)
    buscar_button.grid(column=3, row=0, padx=10, pady=10)

    nombre_label.grid(column=0, row=1, padx=10, pady=10)
    nombre_entry.grid(column=1, row=1, padx=10, pady=10)

    direccion_label.grid(column=2, row=1, padx=10, pady=10)
    direccion_entry.grid(column=3, row=1, padx=10, pady=10)

    telefono_label.grid(column=0, row=2, padx=10, pady=10)
    telefono_entry.grid(column=1, row=2, padx=10, pady=10)

    equipos_label.grid(column=2, row=2, padx=10, pady=10)
    equipos_entry.grid(column=3, row=2, padx=10, pady=10)

    ip_label.grid(column=0, row=3, padx=10, pady=10)
    ip_entry.grid(column=1, row=3, padx=10, pady=10)

    velocidad_label.grid(column=2, row=3, padx=10, pady=10)
    velocidad_entry.grid(column=3, row=3, padx=10, pady=10)

    mensualidad_label.grid(column=0, row=5, padx=10, pady=10)
    mensualidad_entry.grid(column=1, row=5, padx=10, pady=10)



    # Crear un Frame para agrupar los botones
    frame_botones = tk.Frame(vistaRegistro)
    frame_botones.grid(column=0, row=8, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = tk.Button(frame_botones, text="Actualizar", width=25, command=actualizar_cliente_gui)
    guardar.pack(side=tk.LEFT, padx=5)

    eliminar = tk.Button(frame_botones, text="Eliminar", width=25, command=eliminar_datos)
    eliminar.pack(side=tk.LEFT, padx=5)

    # Botón Cancelar
    cancela = tk.Button(frame_botones, text="Cancelar", width=25, command=vistaRegistro.destroy)
    cancela.pack(side=tk.LEFT, padx=5)

    vistaRegistro.mainloop()

