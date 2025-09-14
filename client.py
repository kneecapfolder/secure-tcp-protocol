import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('connected!')

msg = input('Enter your message')
sock.send(msg.encode())

sock.close()
