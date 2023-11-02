import tkinter as tk
from tkinter import scrolledtext
import socket 
import threading 
import Interface
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from datetime import datetime

# Création de la fenêtre principale
root = tk.Tk()
root.title("Live-Chat Python v1.0 (Client)")
root.geometry("470x400")
root.resizable(False, False)

# Chargement de l'image de fond
img = Image.open("chat_wallp2.jpg")
img = img.resize((600,300), Image.LANCZOS)
img = ImageTk.PhotoImage(img)

# Création du widget d'image de fond
fond_label = tk.Label(root, image=img)
fond_label.place(x=0, y=0, relwidth=1, relheight=1)

pseudo = input("Choisissez un pseudo: ")

HOST = '127.0.0.1'
PORT = 18023

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST,PORT))

def write(msg): 
    client.send(msg.encode('utf-8'))
    
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "PSEUDO ":
                client.send(pseudo.encode('utf-8'))
            elif message == "quitter":
                chat_interface.quitte_chat()
                client.close()
                break
            else:
                chat_interface.recieved_message(message)
                print(message)
        except:
            print("Il y a eu une erreur :'( ")
            client.close()
            break

chat_interface = Interface.ChatInterface(root, write) 

# Lancer le thread pour recevoir les messages
receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

# Démarrer la boucle principale de Tkinter
root.mainloop()
