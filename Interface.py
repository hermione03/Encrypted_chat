import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from datetime import datetime


class ChatInterface:
    def __init__(self, master, callback) :
        self.callback = callback
        self.master = master
        master.title("Encrypted chat")
        master.geometry("470x400")
        
         # Zone d'affichage
        self.chat_display = scrolledtext.ScrolledText(master, width=50, height=15, state='disabled')
        self.chat_display.place(x=25, y=40)

        # Création de la zone de saisie
        self.entry = tk.Entry(master, width=65)
        self.entry.place(x=25, y=325)

        # Chargement de l'image pour le bouton "Envoyer"
        self.send_img = Image.open("image.png")
        self.send_img = self.send_img.resize((15, 15), Image.LANCZOS)
        self.send_img = ImageTk.PhotoImage(self.send_img)

        # Création du bouton "envoyer" avec l'image chargée et redimensionnée
        self.send_btn = tk.Button(master, image=self.send_img, command=self.send_message)
        self.send_btn.place(x=400, y=325)

        # Bouton "quitter"
        self.quit_btn = tk.Button(master, text="Quitter", command=self.quitte_chat)
        self.quit_btn.grid(row=2, column=0, padx=5, pady=5)
        self.quit_btn.place(x=210, y=360)


# Lorsque l'utilisateur appuie sur "entrée", le message est envoyé
        self.entry.bind('<Return>', self.send_message)

    def display_message(self,message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert('end', message + '\n')
        #self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.callback(message)


    
    def send_message(self,event=None):
        message = self.entry.get()
        self.entry.delete(0, 'end')
        self.display_message(message)
        #format_message = f'{pseudo}  : {message}'
        #client.send(message.encode('utf-8'))

    def recieved_message(self, message): #permet d'afficher les messages reçus

        # Affichage du message envoyé dans la zone d'affichage
        self.chat_display.configure(state='normal')  # Activation de la zone d'affichage
        self.chat_display.insert('end', f"{message}\n")  # Affichage du message
    
    
    def quitte_chat(self):
        # Désactivation de la saisie de nouveaux messages
        self.entry.config(state='disabled')
        # Désactivation du bouton "quitter"
        self.quit_btn.config(state='disabled')

        self.callback("quitter") #envoie le message quitter a client

        # Affichage d'un message pour indiquer que l'utilisateur a quitté la discussion
        if "Le client a quitté la discussion." not in self.chat_display.get("1.0", "end-1c"):
            # now = datetime.now()
            # timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            self.chat_display.configure(state='normal')  # Activation de la zone d'affichage
            self.chat_display.insert('end', f"Le client a quitté la discussion.\n")  # Affichage du message
            self.chat_display.configure(state='disabled')  # Désactivation de la zone d'affichage
            self.master.destroy()