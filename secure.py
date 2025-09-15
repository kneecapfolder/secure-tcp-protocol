from abc import ABC, abstractmethod
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import struct
import rsa

class SecureBase(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def handshake(self, sock : socket.socket):
        pass
    

    def encrypt(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        cipher_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
        iv = cipher.iv
        return iv, cipher_text


    def decrypt(self, iv, cipher_text):
        decipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = unpad(decipher.decrypt(cipher_text), AES.block_size).decode()
        return plain_text
    

    def send(self, message):
        iv, cipher_text = self.encrypt(message)

        # Send
        self.sock.send(struct.pack('i', len(iv))) # Send iv's length
        self.sock.send(iv) # Send iv
        self.sock.send(cipher_text)


    def recv(self, bytes=1024):
        iv_length, = struct.unpack('i', self.sock.recv(4))
        iv = self.sock.recv(iv_length)
        cipher_text = self.sock.recv(bytes)

        return self.decrypt(iv, cipher_text)



# Server
class SecureServer(SecureBase):
    def __init__(self, HOST, PORT):
        super().__init__()


        self.key = get_random_bytes(16) # Random 128 bit symmetric key
        self.cipher = AES.new(self.key, AES.MODE_CBC)
        
        # server setup
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(1)
        print('listening...')

        self.sock, _ = self.server.accept()
        self.handshake(self.sock)
    

    def handshake(self, sock):
        public_key = rsa.PublicKey.load_pkcs1(sock.recv(1024))
        encrypted_key = rsa.encrypt(self.key, public_key)
        sock.send(encrypted_key)
        self.cipher = AES.new(self.key, AES.MODE_CBC)
        print('agreed on key!')


# Client
class SecureClient(SecureBase):
    def __init__(self, HOST, PORT):
        super().__init__()

        # Setup client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.handshake(self.sock)


    def handshake(self, sock):
        public_key, private_key = rsa.newkeys(256)
        sock.send(public_key.save_pkcs1("PEM"))
        self.key = rsa.decrypt(sock.recv(1024), private_key)
        self.cipher = AES.new(self.key, AES.MODE_CBC)
        print('agreed on key!')
