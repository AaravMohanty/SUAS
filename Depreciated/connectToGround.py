import socket
HOST = "192.168.1.1"
PORT = 49159

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("HI".encode('ascii'))
print(socket.recv(1024))

