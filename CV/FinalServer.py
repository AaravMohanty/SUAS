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

def two_at_once(gps_port, image_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gps_server, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as image_server:
        gps_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        gps_server.bind((host,gps_port))
        gps_server.listen()
        print(f'GPS server listening at {host}:{gps_port}')
        image_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        image_server.bind((host,image_port))
        image_server.listen()
        print(f'Image server listening at {host}:{image_port}')

        # wait for the Pi to connect, then accept the connection
        gps_conn, gps_addr = gps_server.accept() # becomes the new socket
        print('Received and accepted connection to the Pi for GPS server.')
        image_conn, image_addr = image_server.accept()
        print('Received and accepted connection to the Pi for image server.')
        emptymessages = 0
        while True:
            if emptymessages > 1000:
                break
            
            # blocks until at least one connection receives something
            ready_socks,_,_ = select.select((gps_conn, image_conn), [], [])

            for sock in ready_socks:
                
                if sock is gps_conn:
                    data, addr = gps_conn.recvfrom(1024) # max 1024
                    if (data != b''):
                        # decode and keep track of GPS data
                        # format: id,longitude,latitude,altitude,compass_heading
                        last_gps_data = GPSData(data)
                    else:
                        # increment empty counter
                        emptymessages += 1
                elif sock is image_conn:
                    data, addr = image_conn.recvfrom(1024) # max 1024
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
                    print('something went horribly wrong, we got a message from a socket that shouldn\'t exist')

two_at_once(gps_port=GpsPort, image_port=ImagePort)


