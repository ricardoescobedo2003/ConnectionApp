import json
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


def nombre_wisp():


    def guardar_datos():
        # Crear un diccionario con los datos
        datos = {
                "nombre": nombre_wisp_input,
                "mensaje": mensaje
            }

                # Guardar el diccionario en un archivo JSON
        with open("nombre_wisp.json", "w") as file:
                json.dump(datos, file, indent=4)
                messagebox.showinfo("Correcto", "Nombre guardado de manera correcta") 
    
    nombre_wisp_input = simpledialog.askstring("Nombre Wisp", "Ingresa el nombre de wisp, es el que aparecera en tus recibos")
    mensaje = simpledialog.askstring("Mensaje Wisp", "Ingresa el mensaje que quieras que se muestre a tus clientes")

   
    if nombre_wisp_input:
         guardar_datos()
