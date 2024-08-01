from tkinter import *
from tkinter import ttk
from guardar_cliente import registrar_cliente
from datetime import datetime, timedelta
from tkinter import messagebox

equiposA = ["LiteBeam M5 & Router",  "LiteBeam AC & Router",
           "NanoBeam M5 & Router",
           "LiteBeam M5", "LiteBeam AC", "NanoBeam M5",
           "Loco M5"]

velocidades = ["100M/10M", "100M/15M", "100M/20M", "100M/25M", "100M/30M", "100M/50M",
               "100M/60M", "100M/70M", "100M/80M", "100M/90M", "100M/100M",
               "200M/200M", "250M/250M", "300M/300M", "Seleccion Libre"]


mensualidades = ["200", "250", "300", "350", "400", "450", "500"]

def ventana_principal_registro():

    def limpiar():
        nombreEntrada.delete(0, END)
        direccionEntrada.delete(0, END)
        telefonoEntrada.delete(0, END)
        ipEntrada.delete(0, END)
        mensualidadEntrada.delete(0, END)


    def obtenerDatos():
        nombre = nombreEntrada.get()
        direccion = direccionEntrada.get()
        telefono = telefonoEntrada.get()
        equipos = equiposOpciones.get()
        ip = ipEntrada.get()
        velocidad = velocidadOpicones.get()

        fechaActual = datetime.now()
        fechaInstalacion = fechaActual.strftime('%Y-%m-%d')

        proxSuma = fechaActual + timedelta(days=30)
        proximoPago = proxSuma.strftime('%Y-%m-%d')

        mensualidad = mensualidadEntrada.get()
        estado = "activado"
        api = "anotherkey789012"
        registrar_cliente(nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api)
        messagebox.showinfo("Guardado", "Cliente registrado con exito")
        limpiar()

    vistaRegistro = Tk()
    vistaRegistro.title("Registrar cliente")
    vistaRegistro.geometry("700x300")
    vistaRegistro.resizable(False, False)

    nombreLabel = Label(vistaRegistro,
                        text="Nombre Cliente",
                        )
    nombreEntrada = Entry(vistaRegistro,
                          width=25)
    
    nombreLabel.grid(
        column=0,
        row=0,
        padx=10,
        pady=10
    )
    nombreEntrada.grid(
        column=1,
        row=0,
        padx=10,
        pady=10
    )

    direccionLabel = Label(vistaRegistro,
                           text="Direccion"
                           )
    direccionEntrada = Entry(vistaRegistro,
                             width=25)
    
    direccionLabel.grid(
        column=2,
        row=0,
        padx=10,
        pady=10
    )
    direccionEntrada.grid(
        column=3,
        row=0,
        padx=10,
        pady=10
    )

    telefonoLabel = Label(vistaRegistro,
                          text="Telefono"
                          )
    telefonoEntrada = Entry(vistaRegistro,
                            width=25)
    
    telefonoLabel.grid(
        column=0,
        row=1,
        padx=10,
        pady=10
    )
    telefonoEntrada.grid(
        column=1,
        row=1,
        padx=10,
        pady=10
    )

    equiposLabel = Label(vistaRegistro,
                    text="Equipos"
                    )
    equiposOpciones = ttk.Combobox(vistaRegistro,
                                   values=equiposA,
                                   width=25)
    
    equiposLabel.grid(
        column=2,
        row=1,
        padx=10,
        pady=10
    )
    equiposOpciones.grid(
        column=3,
        row=1,
        padx=10,
        pady=10
    )

    ipLabel = Label(vistaRegistro,
                    text="Ip Cliente"
                    )
    ipEntrada = Entry(vistaRegistro,
                      width=25)
    
    ipLabel.grid(
        column=0,
        row=2,
        padx=10,
        pady=10
    )
    ipEntrada.grid(
        column=1,
        row=2,
        padx=10,
        pady=10
    )

    velocidadLabel = Label(vistaRegistro,
                           text="Velocidad")
    velocidadOpicones = ttk.Combobox(vistaRegistro,
                                     values=velocidades,
                                     width=25)
    
    velocidadLabel.grid(
        column=2,
        row=2,
        padx=10,
        pady=10
    )

    velocidadOpicones.grid(
        column=3,
        row=2,
        padx=10,
        pady=10
    )

    mensualidadLabel = Label(vistaRegistro,
                             text="Mensualidad"
                             )
    mensualidadEntrada = ttk.Combobox(vistaRegistro,
                                      values=mensualidades,
                                      width=25)
    
    mensualidadLabel.grid(
        column=0,
        row=3,
        padx=10,
        pady=10
    )
    mensualidadEntrada.grid(
        column=1,
        row=3,
        padx=10,
        pady=10
    )
    
    # Crear un Frame para agrupar los botones
    frame_botones = Frame(vistaRegistro)
    frame_botones.grid(column=0, row=4, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = Button(frame_botones,
                     text="Guardar",
                     width=25,
                     command=obtenerDatos)
    
    guardar.pack(side=LEFT,
                 padx=5)

    # Botón Cancelar
    cancela = Button(frame_botones,
                     text="Cancelar",
                     width=25,
                     command=vistaRegistro.destroy)
    
    cancela.pack(side=LEFT,
                 padx=5)

    vistaRegistro.mainloop()

