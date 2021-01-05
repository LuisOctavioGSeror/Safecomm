from socket import *
import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib
serverPort = 13000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
confirmation = "recived"

#RSA public key and private key
random_generator = Random.new().read
key = RSA.generate(2048,random_generator)
public = key.publickey().exportKey()
private = key.exportKey()

print("Server its waiting to establish a conection...")

connectionSocket, addr = serverSocket.accept()
print("conection established, waiting for key's exchange")
contact_publickey = connectionSocket.recv(4096)
connectionSocket.send(public)


counter = connectionSocket.recv(1024)
connectionSocket.send(confirmation.encode())
key2 = connectionSocket.recv(1024)
connectionSocket.send(confirmation.encode())
print("Server ready to recive: ")

dec = AES.new(key2, AES.MODE_CTR, counter=lambda: counter)
decrypted2 = "none"

while(decrypted2 != b'FINALIZAR'):
    modifiedSentence = connectionSocket.recv(1024)
    decrypted = RSA.importKey(private).decrypt(modifiedSentence)
    decrypted2 = dec.decrypt(decrypted)
    #print(modifiedSentence) encrypted message with AES and RSA
    #print(decrypted) encrypted message with RSA
    print (str(decrypted2))

print('conexao encerrada')
connectionSocket.close()
