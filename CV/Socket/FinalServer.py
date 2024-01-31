# gps needs to be like this --> [image.PIL, [longitude, latitude, altitude]]
# --> list within a list!!!

import socket
import asyncio
import select

host = "192.168.1.1"
ImagePort = 65430
GpsPort = 25250


    
async def listen_gps_coordinates(host, port):
    print(f"Attemping to listen for GPS coordinates on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Gpsserver:
        print(f"Listening for GPS coordinates on {host}:{port}")
        Gpsserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Gpsserver.bind((host,port))
        Gpsserver.listen()
        Gpsconnection, Gpsaddress = Gpsserver.accept()
        print(Gpsserver.getsockname())

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


async def listen_image(host, port):
    print("Attemping Listening to images on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Imageserver:
        print("Listening to images on {host}:{port}")

        Imageserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Imageserver.bind((host,port))
        Imageserver.listen()
        Imageconnection, Imageaddress = Imageserver.accept()

        #Receiving image    
        path = "Downloads\\images"
        totalImage = bytearray
        with Imageconnection:
            file = open(f"{path}\{Tuplelist}.png", "wb")

            while (data := Imageconnection.recv(1024)):
                totalImage += data

            file.write(totalImage)
            file.close


def two_at_once(gps_port, image_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Gpsserver, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Imageserver:
        Gpsserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Gpsserver.bind((host,gps_port))
        Gpsserver.listen()
        Imageserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Imageserver.bind((host,image_port))
        Imageserver.listen()
        while True:
            # blocks until at least one connection receives something
            
            Gpsconnection, Gpsaddress = Gpsserver.accept() # becomes the new socket
            ImageConnection, ImageAddress = Imageserver.accept()
            ready_socks,_,_ = select.select((Gpsconnection, ImageConnection), [], [])

            for sock in ready_socks:
                if sock is Gpsconnection:
                    data, addr = Gpsconnection.recvfrom(1024) # max 1024
                    print(f'Gps server received stuff from {addr}: {data}')
                elif sock is ImageConnection:
                    data, addr = ImageConnection.recvfrom(1024) # max 1024
                    print(f'Image server received stuff from {addr}: {data}')
                else:
                    print('something went horribly wrong')


async def main():
    gps_task = asyncio.create_task(listen_gps_coordinates(host, GpsPort))
    image_task = asyncio.create_task(listen_image(host, ImagePort))


    await gps_task
    await image_task

# asyncio.run(main())
two_at_once(gps_port=GpsPort, image_port=ImagePort)


