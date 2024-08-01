import paramiko
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

def ejecutar_comando(hostname, port, username, password, comando):
    try:
        # Crear instancia de SSHClient
        cliente = paramiko.SSHClient()
        cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectar al dispositivo
        cliente.connect(hostname, port=port, username=username, password=password, look_for_keys=False)
        
        # Ejecutar comando
        stdin, stdout, stderr = cliente.exec_command(comando)
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        
        cliente.close()
        
        if errores:
            return f"Error: {errores}"
        return salida
    except Exception as e:
        return f"Ocurrió un error: {e}"

def obtener_datos():
    # Obtener datos de entrada
    hostname = simpledialog.askstring("IP del Dispositivo", "Ingresa la IP del dispositivo:")
    username = simpledialog.askstring("Usuario", "Ingresa el nombre de usuario:")
    password = simpledialog.askstring("Contraseña", "Ingresa la contraseña:", show='*')
    
    if not hostname or not username or not password:
        messagebox.showerror("Error", "Faltan datos. Por favor, completa todos los campos.")
        return
    
    port = 22  # Puerto por defecto para SSH

    comandos = {
        "01.- Escanear redes aproximas": "iwlist ath0 scan",
        "02.- Lista de estaciones proximas": "iwlist ath0 peers/ap",
        "03.- Rango de potencia soportado y actual": "iwlist ath0 txpower",
        "04.- Lista de canales soportados y actual": "iwlist ath0 frequency/channel",
        "05.- Bitrate actual": "iwlist ath0 bitrate/rate",
        "06.- Autentificaciones y especificaciones": "iwlist ath0 auth",
        "07.- Información sobre la red actual conectada": "iwlist ath0 genie",
        "08.- Interfaces actuales": "ifconfig",
        "09.- Interfaces actuales y su uso": "iwconfig",
        "14.- Encontrar equipamientos conectados": "ubntbox discover"
    }

    # Crear ventana para mostrar resultados
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados")

    text_area = scrolledtext.ScrolledText(ventana_resultados, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # Ejecutar comandos y mostrar resultados
    for descripcion, comando in comandos.items():
        resultado = ejecutar_comando(hostname, port, username, password, comando)
        text_area.insert(tk.END, f"{descripcion}:\n{resultado}\n\n")
        text_area.yview(tk.END)  # Auto scroll al final del texto

# Crear ventana principal
root = tk.Tk()
root.title("Conexión SSH Ubiquiti")

boton_ejecutar = tk.Button(root, text="Obtener Información", command=obtener_datos)
boton_ejecutar.pack(pady=20)

root.mainloop()
