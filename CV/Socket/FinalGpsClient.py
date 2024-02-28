import socket, struct
host = "192.168.1.1"
ImagePort = 25251
GpsPort = 25250
# format of GPS data being sent to groundstation:
# id,longitude,latitude,altitude,compass_heading
gps = b"1,1.2,2,100,200"

import time
import os
#response = os.system("ping -c 1 " + host)
#if response == 0:
#	print(f"{host} is up!")
#else:
#	print(f"{host} is down.")
import sys

def sendMsg(port, data):
    # identify different types of data based on len
    # image packets will have len 1024 for example
    # allows for easy identification of data type - potentially make gps/image handling easier
    msg = struct.pack('>I', len(data), ) + data
    port.sendall(msg)

def sendTermination(port):
    msg = struct.pack('>I', 1024) + 'ENDOFDATA'.encode('ASCII')
    port.sendall(msg)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as imgclient, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gpsclient:
        imgclient.connect((host,ImagePort))
        gpsclient.connect((host,GpsPort))
        
        while True:
            try:
                print(gpsclient.getsockname())
                gpsclient.sendall(gps)
                time.sleep(0.3)
                
                print(imgclient.getsockname())
                img = open('SUAS/CV/GOPR0094.JPG', 'rb')
                # data = img.read(1024)
                # while(data):
                #     print(len(data))
                #     imgclient.send(data)
                #     data = img.read(1024)
                # imgclient.sendall(img.read())
                imgclient.sendall(img)
                # sendTermination(imgclient)
                time.sleep(0.6)
                
                imgclient.shutdown(socket.SHUT_RDWR)
                gpsclient.shutdown(socket.SHUT_RDWR)
                imgclient.close()
                gpsclient.close()
                
                break
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


# based on https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
