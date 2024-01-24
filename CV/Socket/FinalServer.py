# gps needs to be like this --> [image.PIL, [longitude, latitude, altitude]]
# --> list within a list!!!

import socket

host = "127.0.0.1"
ImagePort = 65432
GpsPort = 23456

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Imageserver:
    Imageserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Imageserver.bind((host,ImagePort))
    Imageserver.listen()
    Imageconnection, Imageaddress = Imageserver.accept()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Gpsserver:
    Gpsserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Gpsserver.bind((host,GpsPort))
    Gpsserver.listen()
    Gpsconnection, Gpsaddress = Gpsserver.accept()


with Gpsconnection:
    print(f"Connected by {Gpsaddress}")
    while True:
        data = Gpsconnection.recv(1024)
        if not data:
            break
        Stringgps = bytes.decode(data)

gpslist = Stringgps.split(",")

Listweneed = []  #LIST NOT TUPLE 
for i in gpslist:
    Listweneed.append(float(i))

Tuplelist = tuple(Listweneed)




#Receiving image    
path = "Downloads\\images"
totalImage = bytearray
with Imageconnection:
    file = open(f"{path}\{Tuplelist}.png", "wb")

    while (data := Imageconnection.recv(1024)):
        totalImage += data

    file.write(totalImage)
    file.close


