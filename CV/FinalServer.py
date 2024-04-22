# gps needs to be like this --> [image.PIL, [longitude, latitude, altitude]]
# --> list within a list!!!

import os
import socket, struct
import asyncio
import select
import sys

# caution: path[0] is reserved for script path (or '' in REPL)
print(os.path.abspath(os.path.join(sys.argv[0], "../..")))
sys.path.insert(1, os.path.normpath(os.path.join(sys.argv[0], "../..")))

from Payload import util

# caution: path[0] is reserved for script path (or '' in REPL)
print(os.path.abspath(os.path.join(sys.argv[0], "../..")))
sys.path.insert(1, os.path.normpath(os.path.join(sys.argv[0], "../..")))
from Payload.util import GPSData
import numpy as np
import cv2

host = "192.168.1.1"
if len(sys.argv) > 1:
    host = sys.argv[1]
ImagePort = 25251
GpsPort = 25250

last_gps_data: GPSData = None


def two_at_once(gps_port, image_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gps_server, socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as image_server:
        gps_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        gps_server.bind((host, gps_port))
        gps_server.listen()
        print(f"GPS server listening at {host}:{gps_port}")
        image_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        image_server.bind((host, image_port))
        image_server.listen()
        print(f"Image server listening at {host}:{image_port}")

        # wait for the Pi to connect, then accept the connection
        gps_conn, gps_addr = gps_server.accept()  # becomes the new socket
        print("Received and accepted connection to the Pi for GPS server.")
        image_conn, image_addr = image_server.accept()
        print("Received and accepted connection to the Pi for image server.")
        emptymessages = 0
        while True:
            # blocks until at least one connection receives something
            ready_socks, _, _ = select.select((gps_conn, image_conn), [], [])

            for sock in ready_socks:
                if sock is gps_conn:
                    msg_length = util.read_msg_length(sock)
                    print("gps socket received msg with length " + str(msg_length))
                    if msg_length == 0:
                        print("Received msg with length 0, terminating.")
                        return
                    data = util.read_msg(sock, msg_length)
                    # decode and keep track of GPS data
                    # format: id,longitude,latitude,altitude,compass_heading
                    last_gps_data = GPSData.from_socket_msg(data)
                    print("GPS data received: " + last_gps_data.into_filename())
                elif sock is image_conn:
                    msg_length = util.read_msg_length(sock)
                    print("image socket received msg with length " + str(msg_length))
                    if msg_length == 0:
                        print("Received msg with length 0, terminating.")
                        return
                    img_bytes = read_msg(sock, msg_length)

                    # print('image server got stuff')
                    # PROBLEM:
                    # the three images sent by mainloop are being
                    # rolled up into one - need to be seperated by some logic
                    # cv2 is smart enough to take the 3 images concatenated to each other
                    # and only get the 1st image from the 1st "part" of the data

                    if img_bytes != bytearray():
                        print(f"Image server received image with size {len(img_bytes)}")

                        # save image with most recent GPS data as filename
                        if last_gps_data is not None:
                            # nparray = np.asarray(bytearray(data), dtype="uint8")
                            bytes_to_buffer_img = np.frombuffer(img_bytes, np.uint8)
                            img = cv2.imdecode(bytes_to_buffer_img, cv2.IMREAD_COLOR)
                            os.makedirs("saved-images", exist_ok=True)
                            img_path = os.path.normpath(
                                os.path.join(
                                    os.getcwd(),
                                    "./saved-images/" + last_gps_data.into_filename(),
                                )
                            )
                            print(
                                "Writing image with size "
                                + str(len(bytes_to_buffer_img))
                                + " at "
                                + img_path
                            )
                            write_success = cv2.imwrite(img_path, img)
                            if write_success:
                                print(
                                    "Wrote an image successfully with name: " + img_path
                                )
                            else:
                                print("Failed to write image at path: " + img_path)
                        else:
                            print(
                                "Error: received an image before any GPS data was available, could not save image."
                            )
                    else:
                        # increment empty counter
                        emptymessages += 1
                else:
                    print(
                        "something went horribly wrong, we got a message from a socket that shouldn't exist"
                    )


two_at_once(gps_port=GpsPort, image_port=ImagePort)
