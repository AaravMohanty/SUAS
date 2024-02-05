import socket
host = "192.168.1.1"
ImagePort = 25251
GpsPort = 25250
gps = b"1,1.2,2,100,200"

import time
import os
#response = os.system("ping -c 1 " + host)
#if response == 0:
#	print(f"{host} is up!")
#else:
#	print(f"{host} is down.")
import sys

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as imgclient, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gpsclient:
        imgclient.connect((host,ImagePort))
        gpsclient.connect((host,GpsPort))

        while True:
            try:
                imgclient.sendall(b"some random image")
                time.sleep(0.6)

                gpsclient.sendall(b"some gps data")
                time.sleep(0.3)
            except KeyboardInterrupt:
                print('interrupt')
                imgclient.shutdown(socket.SHUT_RDWR)
                gpsclient.shutdown(socket.SHUT_RDWR)
                imgclient.close()
                gpsclient.close()
                try:
                    sys.exit(130)
                except SystemExit:
                    os._exit(130)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('interrupt')
        imgclient.shutdown()
        gpsclient.shutdown()
        imgclient.close()
        gpsclient.close()
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
