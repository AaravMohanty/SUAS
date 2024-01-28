
import socket
host = "127.0.0.1"
ImagePort = 65432
GpsPort = 23456
gps = b"1,1.2,2,100,200"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host,ImagePort))

    file = open('IMG_1673.jpg', 'rb')
    image_data = file.read(1048576) #FIND SOME BETER WAY TO SEND THE IMAGE

    while image_data:
        client.send(image_data)
        image_data = file.read(1048576) #FIND SOME BETER WAY TO SEND THE IMAGE

    file.close()