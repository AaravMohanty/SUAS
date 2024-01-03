import socket
import numpy as np
import cv2

HOST = '192.168.1.1'
PORT = 25251

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make socket reusable

server.bind((HOST,PORT))
print(server.getsockname())
server.listen(1)

# code for simulating how bytes are parsed when recieved
# takes image, chops it up into blocks of 1024, which
# are added to an array of bytes to be reconstructed babck
# into the same image
"""
testImgData = bytearray()
with open('Downloads\\test3.jpg', 'rb') as f:
    while (data := f.read(1024)):
        testImgData += data

bytesToBuffer = np.frombuffer(testImgData, np.uint8)
testImg = cv2.imdecode(bytesToBuffer, cv2.IMREAD_COLOR)
print(len(bytesToBuffer))
cv2.imwrite("Downloads\\groundstationTesting\\result.jpg", testImg)
"""

while True:
    communication_socket, address = server.accept()

    print(f"Connected to {address}")

    imgBytes = bytearray()
    while (data := communication_socket.recv(1024)):
        imgBytes += data
        # print(data)
    bytesToBufferImg = np.frombuffer(imgBytes, np.uint8)
    testImg2 = cv2.imdecode(bytesToBufferImg, cv2.IMREAD_COLOR)
    cv2.imwrite("Downloads\\groundstationTesting\\result2.jpg", testImg2)

    print(f"Message from client is: received")
    
    communication_socket.send(f"GPS coordinates are: ".encode('ascii'))
    communication_socket.close()
    print(f"Connection with {address} ended.")
