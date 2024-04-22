import socket
import struct
import sys
import os
import time

# caution: path[0] is reserved for script path (or '' in REPL)
print(os.path.abspath(os.path.join(sys.argv[0], "../../..")))
sys.path.insert(1, os.path.normpath(os.path.join(sys.argv[0], "../../..")))

from Payload import util

host = "192.168.1.1"
if len(sys.argv) > 1:
    host = sys.argv[1]
ImagePort = 25251
GpsPort = 25250
test_images = ("IMG_1664.jpg", "IMG_1665.jpg", "IMG_1666.jpg")


# response = os.system("ping -c 1 " + host)
# if response == 0:
# 	print(f"{host} is up!")
# else:
# 	print(f"{host} is down.")

def sendTermination(port):
    msg = struct.pack(">I", 1024) + "ENDOFDATA".encode("ASCII")
    port.sendall(msg)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as imgclient, socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as gpsclient:
        imgclient.connect((host, ImagePort))
        gpsclient.connect((host, GpsPort))
        id = 0

        for filename in test_images:
            try:
                print(gpsclient.getsockname())
                gps = util.GPSData(id, 0, 0, 0, 0)
                util.send_msg(gpsclient, gps.into_socket_msg())
                time.sleep(0.3)

                img = open("./CV/images/" + filename, "rb")
                data = img.read()
                print("sent image with size " + str(len(data)))
                util.send_image(imgclient, gpsclient, data)
                id += 1
            except KeyboardInterrupt:
                print("interrupt")
                imgclient.shutdown(socket.SHUT_RDWR)
                gpsclient.shutdown(socket.SHUT_RDWR)
                imgclient.close()
                gpsclient.close()
                try:
                    sys.exit(130)
                except SystemExit:
                    os._exit(130)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interrupt")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
