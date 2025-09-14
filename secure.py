from abc import ABC, abstractmethod
from Crypto.Cipher import AES
import os
import socket
import rsa

class SecureBase(ABC):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    @abstractmethod
    def handshake(self, sock : socket.socket):
        pass
    
    def encrypt(plain_text):
        pass
        # TODO: AES encryption

    def decrypt(cipher_text):
        pass
        # TODO: AES decryption


# Server
class SecureServer(SecureBase):
    def __init__(self, HOST, PORT):
        super().__init__()

        self.key = os.urandom(64)
        
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        print('listening...')

        self.client, _ = self.sock.accept()
        self.handshake(self.client)
    

    def handshake(self, sock):
        public_key = rsa.PublicKey.load_pkcs1(sock.recv(1024))

        encrypted_key = rsa.encrypt(self.key, public_key)

        sock.send(encrypted_key)


# Client
class SecureClient(SecureBase):
    def __init__(self, HOST, PORT):
        super().__init__()

        self.sock.connect((HOST, PORT))

        self.handshake(self.sock)

    def handshake(self, sock):
        public_key, private_key = rsa.newkeys(256)

        sock.send(public_key.save_pkcs1("PEM"))

        self.key = rsa.decrypt(sock.recv(1024), private_key)