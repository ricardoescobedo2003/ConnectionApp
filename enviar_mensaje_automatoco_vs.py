import sqlite3
import requests
import json
from tkinter import messagebox
import time  # Importar la biblioteca para manejar pausas

def leer_credenciales():
    with open('mensaje_automatico.json', 'r') as archivo:
        datos = json.load(archivo)
    return datos

def enviar_mensaje_automatico(phone_number, text, apikey):
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={text}&apikey={apikey}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Mensaje enviado exitosamente a {phone_number}.")
    else:
        messagebox.showerror("Error al envio", f"Error al enviar el mensaje a {phone_number}: {response.status_code}")

# Función para obtener datos de la base de datos
def obtener_datos_de_base_datos():
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()

    # Consulta para obtener el teléfono y la API para todos los clientes
    cursor.execute("SELECT telefono, api FROM clientes")
    resultados = cursor.fetchall()

    conn.close()

    return resultados

def iniciar_envio_masivo_automatico():
    credenciales = leer_credenciales()
    mensaje = credenciales.get('mensaje', 'Este es un mensaje automático')

    clientes = obtener_datos_de_base_datos()
    
    if clientes:
        mensajes_enviados = 0
        errores = 0

        for i, (phone_number, apikey) in enumerate(clientes):
            if enviar_mensaje_automatico(phone_number, mensaje, apikey):
                mensajes_enviados += 1
            else:
                errores += 1
            
            if (i + 1) % 5 == 0:
                print("Pausando por 5 segundos...")
                time.sleep(5)
        
        # Mostrar notificación de resultado
        messagebox.showinfo("Resultado del Envío", "Mensajes enviados de manera correcta")
    else:
        messagebox.showinfo("Faltan datos", "No se pudo obtener la información necesaria para enviar el mensaje.")
