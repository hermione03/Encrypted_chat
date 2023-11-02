import socket
import threading 


HOST = '127.0.0.1'
PORT = 18023


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()


clients = []
pseudos = []

#envoyer un messages à tous les clients connéctés 
def broadcast(msg):
    for client in clients:
        client.send(msg)
        
        
    
    
# enovoie aux autre client ce qu'un client un envoyé 
def handle(client):
    while True :
        if(len(clients) == 0):
            break
        try: 
            message = client.recv(1024) # si tu reçois un message
            index = clients.index(client)
            pseudo = pseudos[index]
            broadcast(message) #envoyer ce message à tous les autres clients 
        except:
            index = clients.index(client)
            clients.remove(client)
            pseudo = pseudos[index]
            broadcast(f'{pseudo} a quitté le chat'.encode('utf-8'))
            pseudos.remove(pseudo)
            break
            
            
            
def receive():
    while True:
        client, address = server.accept()
        print("Nouvelle connection de",str(address))
        client.send("PSEUDO ".encode('utf-8'))
        pseudo = client.recv(1024).decode('utf-8')
        pseudos.append(pseudo)
        clients.append(client)
        
        
        print(f"Le pseudo du client est : {pseudo} !")
        broadcast(f"{pseudo} a rejoin la conversation ".encode("utf-8"))
        client.send("Vous etes connecté au serveur ! ".encode("utf-8"))
        
        thread = threading.Thread(target = handle, args=(client,))
        thread.start()
        
        
receive()