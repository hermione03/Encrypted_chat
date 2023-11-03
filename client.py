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

#pseudo = input("Choisissez un pseudo: ")
#pseudo = ""  # Initialiser la variable pseudo


HOST = '127.0.0.1'
PORT = 18023

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# def connect_to_server():
    
    #return pseudo
    #connect_to_server()
# def get_pseudo():
#     global pseudo
#     pseudo = pseudo_entry.get()
#     print(pseudo)
#     pseudo_entry.config(state='disabled')  # Désactiver le champ d'entrée après avoir obtenu le pseudo
    
    
client.connect((HOST, PORT))
    

# # Champ d'entrée pour le pseudo
# pseudo_label = tk.Label(root, text="Choisissez un pseudo:")
# pseudo_label.place(x=25, y=10)
# pseudo_entry = tk.Entry(root, width=30)
# pseudo_entry.place(x=160, y=10)
# pseudo_button = tk.Button(root, text="Valider", command=get_pseudo)
# pseudo_button.place(x=340, y=8)
# #     global pseudo
#     client.connect((HOST, PORT))
#     client.send(f"PSEUDO {pseudo}".encode('utf-8'))



def write(msg): 
    client.send(msg.encode('utf-8'))
    
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            # if message == "PSEUDO ":
            #     chat_interface.get_pseudo()
                #print(pseudo)
            #     #client.send(pseudo.encode('utf-8'))
            #     write(pseudo)
                #chat_interface.recieved_message(pseudo)
            #     #connect_to_server()
            if message == "quitter":
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
