import socket
import threading
import time 


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

HOST = '127.0.0.1'
PORT = 18023


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(2)

print("Serveur en ecoute")

server_actif = True



clients = []
pseudos = []





        
        
def broadcast(msg, client):
    for other_client in clients:
        if other_client != client and other_client.fileno() != -1:
            index = clients.index(client)
            print(index)
            pseudo = pseudos[index]
            print(pseudo)
            txt = str(msg, 'utf-8')
            test = f'{pseudo} : {txt}'
            other_client.send(test.encode())


# Echange de cles Diffie-Hellman 
def exchange_keys(client1, client2):
    client1.send("PK".encode('utf-8')) #demander Pa = g^a mod p
    client1_public_key = client1.recv(9000).decode('utf-8')  #il les recupére dans des variables
    client1_public_key =  str(client1_public_key.split()[1])
    print(f"client1_public_key :{client1_public_key}")
    client2.send("PK".encode('utf-8')) #demander Pb = g^b mod p
    client2_public_key = client2.recv(9000).decode('utf-8')#il les recupére dans des variables
    client2_public_key =  str(client2_public_key.split()[1])
    print(f"client2_public_key :{client2_public_key}")
    
    #Puis les reenvoie comme il faut
    client1.send(f"FK {client2_public_key}".encode('utf-8'))
    client2.send(f"FK {client1_public_key}".encode('utf-8'))     


    
    
# enovoie aux autre client ce qu'un client un envoyé 
def handle(client):
    global server_actif 
    while True :
        try:
            message = client.recv(9000) # si tu reçois un message
            if str(message, 'utf-8') == 'quitter':
                index = clients.index(client)
                clients.remove(client)
                pseudo = pseudos[index]
                broadcast(f'{pseudo} a quitté le chat'.encode('utf-8'),client)
                pseudos.remove(pseudo)
                if(len(clients) == 0):
                    print("Tous les clients sont déconnectés. Fermeture du serveur.")
                    server_actif = False
                    break
            else:
                if(not(message.startswith(b"Pk"))):
                    index = clients.index(client)
                    pseudo = pseudos[index]
                    broadcast(message,client) #envoyer ce message à tous les autres clients 
        except Exception as e:
            print(f"Erreur dans le gestionnaire : {e}")
            index = clients.index(client)
            clients.remove(client)
            pseudo = pseudos[index]
            broadcast(f'{pseudo} a quitté le chat'.encode('utf-8'),client)
            pseudos.remove(pseudo)
            break        
            
            
def receive():
    session = True
    global server_actif 
    while server_actif:
        client, address = server.accept()
        print("Nouvelle connection de",str(address))
        client.send("PSEUDO ".encode('utf-8'))
        pseudo = client.recv(9000).decode('utf-8')
        pseudos.append(pseudo)
        print(pseudo)
        clients.append(client)
    
        
        
        print(f"Le pseudo du client est : {pseudo} !")
        broadcast(f"{pseudo} a rejoint la conversation ".encode("utf-8"),client)
        client.send("Vous etes connecté au serveur ! ".encode("utf-8"))
        
        if len(clients) == 2 and session :
            print("session\n")
            exchange_keys(clients[0], clients[1])
            session = False
            time.sleep(30)
        thread = threading.Thread(target = handle, args=(client,))
        thread.start()
    server.close()
        
        
receive()