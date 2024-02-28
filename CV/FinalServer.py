# gps needs to be like this --> [image.PIL, [longitude, latitude, altitude]]
# --> list within a list!!!

import os
import socket, struct
import asyncio
import select
import numpy as np
import cv2

host = "127.0.0.1"
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
        Format: id-longitude-latitude-altitude-heading.jpg
        """
        filename = f'{self.id}-{self.longitude}-{self.latitude}-{self.altitude}-{self.heading}'
        return filename.replace(".", "_") + ".jpg"

last_gps_data: GPSData = None

# def recvData(server, numBytes):
#     data = bytearray()
#     while len(data) < numBytes:
#         addData = server.recv(numBytes - len(data))
#         if not addData:
#             return None
#         data.extend(addData)
#     return data
    
# def recv_msg(port):
#     # get length of packet
#     msgLen = recvData(port, 4)
#     if not msgLen:
#         return None
#     # parse data after the length header
#     # unpack returns a tuple - get index 0 to get actual data
#     msglen = struct.unpack('>I', msgLen)[0]
#     return recvData(port, msglen)


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
                        print(last_gps_data.into_filename())
                    else:
                        # increment empty counter
                        emptymessages += 1
                elif sock is image_conn:
                    # print(image_conn.getsockname())
                    # print("image server receiving data!")                    
                    addr = None
                    img_bytes = bytearray()
                    while (data := image_conn.recvfrom(262144))[0]:
                        print(len(data[0]))
                        img_bytes += data[0]
                        addr = data[1]
                        
                    # if(img_bytes is not None):
                    #     print(len(img_bytes))
                    #     bytes_to_buffer_img = np.frombuffer(img_bytes, np.uint8)
                    #     print(len(bytes_to_buffer_img))
                    #     print(bytes_to_buffer_img)
                    #     img = cv2.imdecode(bytes_to_buffer_img, cv2.IMREAD_UNCHANGED)
                    #     # print(img.shape())
                    #     cv2.imwrite('./images/' + last_gps_data.into_filename(), img)
                    #     print("Wrote a file with name: " + last_gps_data.into_filename())


                    # data, addr = image_conn.recvfrom(67108864) # max 1024
                    if (img_bytes != bytearray()):
                        print(f'Image server received image from {addr} with size {len(img_bytes)}')
                        
                        
                        # save image with most recent GPS data as filename
                        if (last_gps_data is not None):
                            # nparray = np.asarray(bytearray(data), dtype="uint8")
                            bytes_to_buffer_img = np.frombuffer(img_bytes, np.uint8)
                            img = cv2.imdecode(bytes_to_buffer_img, cv2.IMREAD_COLOR)
                            os.makedirs('saved-images', exist_ok=True)
                            img_path = os.path.normpath(os.path.join(os.getcwd(), "./saved-images/" + last_gps_data.into_filename()))
                            print("Writing image with size " + str(len(bytes_to_buffer_img)) + " at " + img_path)
                            cv2.imwrite(img_path, img)
                            print("Wrote an image with name: " + img_path)
                        else:
                            print("Error: received an image before any GPS data was available, could not save image.")
                    else:
                        # increment empty counter
                        emptymessages += 1
                else:
                    print('something went horribly wrong, we got a message from a socket that shouldn\'t exist')



two_at_once(gps_port=GpsPort, image_port=ImagePort)


