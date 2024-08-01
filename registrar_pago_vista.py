import sqlite3
from tkinter import *
from tkinter import ttk
from registrar_pago import registrar_pago_recibo
from datetime import *
from tkinter import messagebox

# Función para buscar cliente por ID y rellenar los widgets Entry
def buscar_cliente_por_id(id_cliente):
    cliente_id = id_cliente
    if not cliente_id:
        messagebox.showerror("Error", "Por favor, ingresa un ID de cliente.")
        return

    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, ip, mensualidad FROM clientes WHERE id=?', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        nombre_entry.delete(0, END)
        nombre_entry.insert(0, cliente[0])

        ip_entry.delete(0, END)
        ip_entry.insert(0, cliente[1])

        mensualidad_entry.delete(0, END)
        mensualidad_entry.insert(0, cliente[2])

    else:
        messagebox.showinfo("Información", "Cliente no encontrado.")

def obtener_datos_registrar_pago():
    nombreCliente = nombre_entry.get()
    mensualidad = mensualidad_entry.get()
        
    fechaActual = datetime.now()
    fechaPago = fechaActual.strftime('%Y-%m-%d')

    proxSuma = fechaActual + timedelta(days=30)
    proximoPago = proxSuma.strftime('%Y-%m-%d')

    registrar_pago_recibo(nombreCliente, mensualidad, fechaPago, proximoPago)
    print(nombreCliente, mensualidad, fechaPago, proximoPago)

def ventana_buscar_cliente_pagar():
    def obtener_datos():
        id_cliente = id_entry.get()        
        buscar_cliente_por_id(id_cliente)

    global id_entry, nombre_entry, direccion_entry, telefono_entry, equipos_entry, ip_entry, velocidad_entry, fecha_instalacion_entry, proximo_pago_entry, mensualidad_entry, estado_entry, api_entry

    vistaRegistro = Tk()
    vistaRegistro.title("Registrar Pago")
    vistaRegistro.geometry("600x200")
    vistaRegistro.resizable(False, False)

    id_label = Label(vistaRegistro, text="Id del Cliente")
    id_entry = Entry(vistaRegistro, width=20)

    buscar_button = Button(vistaRegistro, text="Buscar", width=20, command=obtener_datos)

    nombre_label = Label(vistaRegistro, text="Nombre Cliente")
    nombre_entry = Entry(vistaRegistro, width=20)

    ip_label = Label(vistaRegistro, text="Ip Cliente")
    ip_entry = Entry(vistaRegistro, width=20)

    mensualidad_label = Label(vistaRegistro, text="Mensualidad")
    mensualidad_entry = Entry(vistaRegistro, width=20)


    id_label.grid(column=0, row=0, padx=10, pady=10)
    id_entry.grid(column=1, row=0, padx=10, pady=10)
    buscar_button.grid(column=3, row=0, padx=10, pady=10)

    nombre_label.grid(column=0, row=1, padx=10, pady=10)
    nombre_entry.grid(column=1, row=1, padx=10, pady=10)

    ip_label.grid(column=2, row=1, padx=10, pady=10)
    ip_entry.grid(column=3, row=1, padx=10, pady=10)

    mensualidad_label.grid(column=0, row=2, padx=10, pady=10)
    mensualidad_entry.grid(column=1, row=2, padx=10, pady=10)

    # Crear un Frame para agrupar los botones
    frame_botones = Frame(vistaRegistro)
    frame_botones.grid(column=0, row=8, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = Button(frame_botones, text="Registrar Pago", width=25, command=obtener_datos_registrar_pago)
    guardar.pack(side=LEFT, padx=5)
    # Botón Cancelar
    cancela = Button(frame_botones, text="Cancelar", width=25, command=vistaRegistro.destroy)
    cancela.pack(side=LEFT, padx=5)

    vistaRegistro.mainloop()

