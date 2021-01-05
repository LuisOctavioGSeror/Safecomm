from socket import *
import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib
import time
serverName = "localhost"
serverPort = 13000
sentence = "none"


#RSA public key and private key
random_generator = Random.new().read
key = RSA.generate(2048,random_generator)
public = key.publickey().exportKey()
private = key.exportKey()


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
clientSocket.send(public)
contact_publickey = clientSocket.recv(4096)


#AES keys may be 128 bits (16 bytes), 192 bits (24 bytes) or 256 bits (32 bytes) long.
key2 = os.urandom(32)
counter = os.urandom(16)
enc = AES.new(key2, AES.MODE_CTR, counter=lambda: counter)


clientSocket.send(counter)
CounterConfirmation = clientSocket.recv(1024)
clientSocket.send(key2)
KeyConfirmation = clientSocket.recv(1024)


if (CounterConfirmation.decode() == "recived" and KeyConfirmation.decode() == "recived"):

  while(sentence != 'FINALIZAR'):
    sentence = input('Digite aqui: ')
    ensentence = enc.encrypt(sentence)
    encrypted = RSA.importKey(contact_publickey).encrypt(ensentence,None)
    #print(encrypted) only if you wanna see the encrypted message
    clientSocket.send(encrypted[0])

else:

  print("faltando chave de confirmação")


print("conexao encerrada")
clientSocket.close()
