import tkinter as tk
from tkinter import scrolledtext
import socket 
import threading 
import Interface
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from datetime import datetime

import random
import socket
import sys 
import threading 
import hashlib
import os
from binascii import hexlify

import nacl.secret 
import nacl.utils 



#generation de cles publique et privée du client
#privée : a/b
def genRandom(bits):
    bytes = bits // 8 + 1#nb d'octets
    rand = int(hexlify(os.urandom(bytes)), 16)
    #rand = random.randint(2, 10)
    return rand

sk = genRandom(256)

#envoyer une demande de recevoir p et g ? 
#recuper p et g


p= 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF

g = 2


# #fonction qui calcule P
def genPubKey(pk,p,g):
    print("generation de cle publique : g^(a/b) mod p \n")
    return pow(g, pk, p)# g^(private_key) mod p


def genShared(fk,p,k):
    # print("generation de cle partagée : P^(a/b) mod p \n")
    # return pow(fk, k, p)# P^(private_key) mod p
    sharedSecret = pow(fk, k, p)
    _sharedSecretBytes = str(sharedSecret).encode('utf-8')
    s = hashlib.sha256()
    s.update(bytes(_sharedSecretBytes))
    key = s.digest()
    return key


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

global box, Key
Key = 0
box = None


    
def receive():
    global box
    while True:
        try:
            message = client.recv(9000)
            if message == b"PK":
                Pk = pow(g, sk, p)
                public_key = f"Pk {Pk}"
                print(f"Pk : {Pk}")
                client.send(str(public_key).encode('utf-8'))
            elif message.startswith(b"FK"):
                Fk = int(message.split()[1])
                print(f"Le serveur a envoyé la valeur de P de l'autre client : {Fk}")
                print("sk : ", sk)
                print(sys.getsizeof(sk))
                Key = genShared(Fk, p, sk)
                print(f"La clé partagée est : {Key}")
                print(sys.getsizeof(Key))
                box = nacl.secret.SecretBox(Key)
            elif message == "quitter":
                chat_interface.quitte_chat()
                client.close()
                break
            else:
                if box is not None:
                    print("Decrypt")
                    decrypted = box.decrypt(message)
                    print(decrypted.decode())
                
                chat_interface.recieved_message(message)
                    # print(message.decode())
        except Exception as e:
            print(f"Erreur dans le gestionnaire : {e}")
            client.close()
            break
    
def write(msg):
    global box
    if (msg.startswith("PSEUDO")):
        client.send(msg.split()[1].encode('utf-8'))
        
    else:
        print("Encrypt")
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        encrypted = box.encrypt(msg.encode(),nonce)
    # client.send(str(encrypted).encode('utf-8'))
    
        client.send(encrypted)
        print(f"envoyé {encrypted}")
            

chat_interface = Interface.ChatInterface(root, write) 

# Lancer le thread pour recevoir les messages
receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

# Démarrer la boucle principale de Tkinter
root.mainloop()
