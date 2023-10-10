import socket

HOST = '10.123.251.222'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(1)

while True:
    communication_socket, address=server.accept()
    print(f"Connected to {address}")
    message=communication_socket.recv(1024).decode('ascii')
    print(f"Message from client is:{message}")
    communication_socket.send(f"Message received".encode('ascii'))
    communication_socket.close()
    print(f"Connection with {address} ended.")
