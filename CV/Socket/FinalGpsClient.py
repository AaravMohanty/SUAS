import socket
host = "192.168.1.1"
ImagePort = 65430
GpsPort = 25250
gps = b"1,1.2,2,100,200"

import os
response = os.system("ping -c 1 " + host)
if response == 0:
	print(f"{host} is up!")
else:
	print(f"{host} is down.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host,GpsPort))
    client.sendall(gps)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	client.connect((host, ImagePort))
	client.sendall(b"random image idk")
