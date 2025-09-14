import socket
import secure

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

server = secure.SecureServer(HOST, PORT)
