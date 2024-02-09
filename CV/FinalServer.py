# gps needs to be like this --> [image.PIL, [longitude, latitude, altitude]]
# --> list within a list!!!

import socket
import asyncio
import select

host = "192.168.1.1"
ImagePort = 25251
GpsPort = 25250

class GPSData:
    """
    GPS data received from the Raspberry Pi on the drone.
    """
    id = int
    longitude = float
    latitude = float
    altitude = float
    heading = float

    def __init__(self, socket_msg: bytes) -> None:
        """
        Decode GPS data from a socket message.
        Format: id,longitude,latitude,altitude,compass_heading
        """
        # convert bytes to string
        data_str = socket_msg.decode()
        # now it looks like 1,2,3,4,5
        # split it by commas into a list of strings
        num_strings = data_str.split(',')
        # loop through and convert to numbers
        gps_data_vals = list(map(float, num_strings))
        self.id = int(gps_data_vals[0])
        self.longitude = gps_data_vals[1]
        self.latitude = gps_data_vals[2]
        self.altitude = gps_data_vals[3]
        self.heading = gps_data_vals[4]
    
    def into_filename(self) -> str:
        """
        Return a file name with the GPS data.
        Format: id,longitude,latitude,altitude,heading.jpg
        """
        format_str = '{id},{long},{lat},{alt},{head}.jpg'
        return format_str.format(
            id=id, 
            long=self.longitude, 
            lat = self.latitude, 
            alt = self.altitude, 
            head = self.heading)
    
last_gps_data: GPSData = None
    
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
        print('listening rn')
        Gpsconnection, Gpsaddress = Gpsserver.accept() # becomes the new socket
        ImageConnection, ImageAddress = Imageserver.accept()
        print('received and accepted connections')
        emptymessages = 0
        while True:
            if emptymessages > 1000:
                break
            
            # blocks until at least one connection receives something
            ready_socks,_,_ = select.select((Gpsconnection, ImageConnection), [], [])

            for sock in ready_socks:
                
                if sock is Gpsconnection:
                    data, addr = Gpsconnection.recvfrom(1024) # max 1024
                    if (data != b''):
                        # decode and keep track of GPS data
                        # format: id,longitude,latitude,altitude,compass_heading
                        last_gps_data = GPSData(data)

                        # save a file with name:
                        # id,longitude,latitude,altitude,heading.jpg
                    else:
                        # increment empty counter
                        emptymessages += 1
                elif sock is ImageConnection:
                    data, addr = ImageConnection.recvfrom(1024) # max 1024
                    if (data != b''):
                        print(f'Image server received stuff from {addr}: {data}')
                        
                        # save image with most recent GPS data as filename
                        if (last_gps_data is not None):
                            print("Pretended to write a file with name: " + last_gps_data.into_filename())
                        else:
                            print("Error: received an image before any GPS data was available, could not save image.")
                    else:
                        # increment empty counter
                        emptymessages += 1
                else:
                    print('something went horribly wrong')


async def main():
    gps_task = asyncio.create_task(listen_gps_coordinates(host, GpsPort))
    image_task = asyncio.create_task(listen_image(host, ImagePort))


    await gps_task
    await image_task

# asyncio.run(main())
two_at_once(gps_port=GpsPort, image_port=ImagePort)


