import json
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


def definir_mensaje_automatico():


    def guardar_datos():
        # Crear un diccionario con los datos
        datos = {
                "mensaje": mensaje
            }

                # Guardar el diccionario en un archivo JSON
        with open("mensaje_automatico.json", "w") as file:
                json.dump(datos, file, indent=4)
                messagebox.showinfo("Mensaje Bot", "Mensaje guardado de manera correcta") 
    
    mensaje = simpledialog.askstring("Mensaje Wisp", "Ingresa el mensaje que quieras que se envie a tus clientes")

   
    if mensaje:
         guardar_datos()
