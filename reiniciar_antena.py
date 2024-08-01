import paramiko
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

def reiniciar_antenna(hostname, username, password):
    # Crear una instancia de SSHClient
    client = paramiko.SSHClient()
    
    # Cargar las claves del sistema
    client.load_system_host_keys()
    
    # Añadir la clave del host si no está ya en el archivo known_hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conectar al dispositivo
        client.connect(hostname, username=username, password=password)
        
        # Ejecutar el comando de reinicio
        stdin, stdout, stderr = client.exec_command('reboot')
        
        # Esperar a que el comando se ejecute
        stdout.channel.recv_exit_status()
        
        # Imprimir la salida del comando (si es necesario)
        messagebox.showinfo("Reinicio", "La antena se reinicio de manera correcta")
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        
    finally:
        # Cerrar la conexión SSH
        client.close()


def reiniciar():
    host = simpledialog.askstring("Ip Ubiquiti", "Ingresa la ip de la antena a reiniciar")
    usuario = simpledialog.askstring("Usuario Ubiquiti", "Ingresa el usuario de la antena a reiniciar")
    password = simpledialog.askstring("Password Ubiquiti", "Ingresa la password de la antena a reiniciar")

    hostname = host
    username = usuario
    reiniciar_antenna(hostname, username, password)

