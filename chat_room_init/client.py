import random
import socket
import sys 
import threading 
import hashlib
import os
from binascii import hexlify

import nacl.secret 
import nacl.utils 



# from Crypto.Util.Padding import pad, unpad
# from Crypto.Cipher import AES
# from base64 import b64decode
# from base64 import b64encode
# from Crypto import Random
# from Crypto.Random import get_random_bytes

# BLOCK_SIZE = 16  # Bytes
# pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
#                 chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]


# def encrypt(raw,key):
#         raw = pad(raw)
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(key, AES.MODE_CBC, iv)
#         return b64encode(iv + cipher.encrypt(raw))

# def decrypt(enc,key):
#     enc = b64decode(enc)
#     iv = enc[:16]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     return unpad(cipher.decrypt(enc[16:])).decode('utf8')



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



pseudo = input("Choisissez un pseudo: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 18023
client.connect((HOST, PORT))

global box, Key
Key = 0
box = None

def receive():
    global box
    while True:
        try:
            message = client.recv(9000)
            if message == b"PSEUDO ":
                client.send(str(pseudo).encode('utf-8'))
            elif message == b"PK":
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
            else:
                if box is not None:
                    decrypted = box.decrypt(message)
                    print(decrypted.decode())
                else:
                    print(message.decode())
        except Exception as e:
            print(f"Erreur dans le gestionnaire : {e}")
            client.close()
            break

def write():
    global box
    while True:
        message = f'{pseudo} : {input("")}'
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        encrypted = box.encrypt(message.encode(),nonce)
        # client.send(str(encrypted).encode('utf-8'))
        
        client.send(encrypted)
        print(f"envoyé {encrypted}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()









