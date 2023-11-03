import socket
import threading 




HOST = '127.0.0.1'
PORT = 18023


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

print("Serveur en ecoute")

server_actif = True

#* Generer p et q

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
            other_client.send(test.encode('utf-8'))

        


    
    
# enovoie aux autre client ce qu'un client un envoyé 
def handle(client):
    global server_actif 
    while True :
        message = client.recv(1024) # si tu reçois un message
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
            index = clients.index(client)
            pseudo = pseudos[index]
            broadcast(message,client) #envoyer ce message à tous les autres clients 
            
            
            
def receive():
    global server_actif 
    while server_actif:
        client, address = server.accept()
        print("Nouvelle connection de",str(address))
        client.send("PSEUDO ".encode('utf-8'))
        pseudo = client.recv(1024).decode('utf-8')
        pseudos.append(pseudo)
        print(pseudo)
        clients.append(client)
    
        
        
        print(f"Le pseudo du client est : {pseudo} !")
        broadcast(f"{pseudo} a rejoint la conversation ".encode("utf-8"),client)
        client.send("Vous etes connecté au serveur ! ".encode("utf-8"))
        
        thread = threading.Thread(target = handle, args=(client,))
        thread.start()
    server.close()
        
        
receive()