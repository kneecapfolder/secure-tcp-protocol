import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print('listening...')

client, addr = server.accept()
msg = client.recv(1024).decode()
print(msg)

client.close()
server.close()