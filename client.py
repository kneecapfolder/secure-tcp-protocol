import socket
import secure

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

sock = secure.SecureClient(HOST, PORT)
