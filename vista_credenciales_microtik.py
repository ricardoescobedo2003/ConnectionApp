from tkinter import *
import json
from tkinter import messagebox

def vista_credenciales():
    vista = Tk()
    vista.title("Credenciales Microtik")
    vista.geometry("600x150")
    vista.resizable(False, False)

    def get_datos():
        usuario = entUsuario.get()
        password = entPassword.get()
        ip = entIp.get()

        # Crear un diccionario con los datos
        datos = {
            "usuario": usuario,
            "password": password,
            "ip": ip
        }

        # Guardar el diccionario en un archivo JSON
        with open("credenciales.json", "w") as file:
            json.dump(datos, file, indent=4)
            messagebox.showinfo("Correcto", "Credenciales guardadas") 

    lbUsuario = Label(vista, text="Usuario:")
    entUsuario = Entry(vista, width=25)

    lbIp = Label(vista, text="Ip:")
    entIp = Entry(vista, width=25)

    lbPassword = Label(vista, text="Password: ")
    entPassword = Entry(vista, width=25)

    lbUsuario.grid(row=0, column=0, padx=10, pady=10)
    entUsuario.grid(row=0, column=1, padx=10, pady=10)

    lbIp.grid(row=0, column=2, padx=10, pady=10)
    entIp.grid(row=0, column=3, padx=10, pady=10)

    lbPassword.grid(row=1, column=0, padx=10, pady=10)
    entPassword.grid(row=1, column=1, padx=10, pady=10)

    frame_botones = Frame(vista)
    frame_botones.grid(column=0, row=4, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = Button(frame_botones,
                     text="Guardar",
                     width=25,
                     command=get_datos)
    
    guardar.pack(side=LEFT,
                 padx=5)

    # Botón Cancelar
    cancela = Button(frame_botones,
                     text="Cancelar",
                     width=25,
                     command=vista.destroy)
    
    cancela.pack(side=LEFT,
                 padx=5)

    vista.mainloop()
