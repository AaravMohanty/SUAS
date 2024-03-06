import socket

HOST = '10.123.251.222'
PORT = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Hi".encode('ascii'))
print(socket.recv(1024))
