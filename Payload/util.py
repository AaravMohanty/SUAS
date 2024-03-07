# TO BE TESTED
# this is supposed to be a refactor of the current codebase, for the purposes of centralizing everything
# goals of this file are centralization, implmenting multithreading/multiprocessing, have the main loop that will be running during flight

# imports
import sys
import requests, json, time, threading, os, subprocess, math
from open_gopro import WirelessGoPro
from PIL import Image
import math
import asyncio
from mavsdk import System
from subprocess import check_output
import socket

# from pythonping import ping


class GPSData:
    """
    GPS data received from the Raspberry Pi on the drone.
    """

    id = int
    longitude = float
    latitude = float
    altitude = float
    heading = float

    def __init__(self, id: int, long: int, lat: int, alt: int, head: int) -> None:
        self.id = id
        self.longitude = long
        self.latitude = lat
        self.altitude = alt
        self.heading = head

    @classmethod
    def from_socket_msg(cls, socket_msg: bytes) -> None:
        """
        Decode GPS data from a socket message.
        Format: id,longitude,latitude,altitude,compass_heading
        """
        # convert bytes to string
        data_str = socket_msg.decode()
        # now it looks like 1,2,3,4,5
        # split it by commas into a list of strings
        번호 = data_str.split(",")
        # loop through and convert to numbers
        gps_data_vals = list(map(float, 번호))
        id = int(gps_data_vals[0])
        lng = gps_data_vals[1]
        lat = gps_data_vals[2]
        alt = gps_data_vals[3]
        head = gps_data_vals[4]
        return cls(id, lng, lat, alt, head)

    def into_filename(self) -> str:
        """
        Return a file name with the GPS data.
        Format: id-longitude-latitude-altitude-heading.jpg
        """
        filename = (
            f"{self.id}-{self.longitude}-{self.latitude}-{self.altitude}-{self.heading}"
        )
        return filename.replace(".", "_") + ".jpg"

    def into_socket_msg(self) -> bytes:
        """
        Return a bytestring in the format id,longitude,latitude,altitude,compass_heading
        """
        return (
            f"{self.id},{self.longitude},{self.latitude},{self.altitude},{self.heading}"
        ).encode("ascii")


# globals
ip = "http://10.5.5.9:8080"  # adress of the gopro
host = "192.168.1.1"  # adress of the groundstation
GpsPort = 25250
ImagePort = 25251


# takes an image with the gopro using the http requests specified by the open gopro API
def getImage():
    # set to photo mode
    command = "/gopro/camera/set_group?id=1001"
    requests.get(url=ip + command)
    # take photo
    command = "/gopro/camera/shutter/start"
    requests.get(url=ip + command)

    # waits for busy flag to be set to false
    print("gopro busy for " + str(waitForCamera()) + "seconds.")

    # grab the file directory currently on the gopro
    command = "/gopro/media/list"
    r = requests.get(url=ip + command)

    json = r.json()
    # grab most recently taken media file, regardless of format
    recent = json["media"][0]["fs"][-1]["n"]
    # download most recent media file
    command = "/videos/DCIM/100GOPRO/" + recent
    r = requests.get(url=ip + command)
    # print(type(r.content))
    # i = BytesIO(r.content)
    return r.content


# Waits until the camera is ready to recieve further commands. returns the number of seconds teh camera was busy for
def waitForCamera():
    # grab state dictionary of the gopro
    command = "/gopro/camera/state"
    busytime = 0
    response = requests.get(url=ip + command)
    # read off the busy status of the camrea. If the status is 1, the camera is busy
    while response.json()["status"]["8"] == 1:
        time.sleep(0.1)
        busytime += 0.1
        response = requests.get(url=ip + command)
    return busytime


# connects to the gopro AP with the wifi interface specified. default interface is wlan0
# utilizes open-gopro api to activate wifi ap on gopro. However, when trying to connect to said AP the open-gopro API fails, hence the need for nmcli
def connectToCamera(iface="wlan0"):
    # create gopro object
    gopro = WirelessGoPro(enable_wifi=False)
    print("opening GoPro Bluetooth connection..")
    gopro.open()

    print("bluetooth connected to GoPro")
    gopro.ble_command.enable_wifi_ap(enable=True)
    print("wifi AP enabled on GoPro")
    gopro.close()
    print("Bluetooth connection closed")
    # update list of available wifi networks. may take a second
    os.system("sudo nmcli dev wifi rescan")
    connected = os.system(
        'nmcli dev wifi connect "HERO10 Black" password psY-mjc-Z+F ifname ' + iface
    )
    while (
        connected == 2560
    ):  # 2560 is the error code that is returned when nmcli cannot connect to the gopro, so this is essentially "while cannot find the gopro"
        print("retrying")
        time.sleep(5)
        os.system("sudo nmcli dev wifi rescan")
        connected = os.system(
            'nmcli dev wifi connect "HERO10 Black" password psY-mjc-Z+F ifname ' + iface
        )
        # this loop usually takes around 2-4 tries to find it, so dont freak out if it cant find it immediately


def keepAlive(interval):
    while True:
        response = requests.get(url="http://10.5.5.9:8080/gopro/camera/keep_alive")
        time.sleep(interval)
        print("sent keep-alive with status " + str(response.status_code))
        if finished:
            break


# project the 3-d gps coordinate onto a 2-d plane, allowing us to use a polygonization algorithm for finding the shortest path between nodes
def projectOntoPlane(lang, long):
    rho = 3, 958.8
    x = rho * math.sin(long) * math.cos(lang)
    y = rho * math.sin(long) * math.sin(lang)

    r = math.sqrt(x**2 + y**2)
    theta = math.atan(y / x)
    return (r, theta)


def calcDistance(coords1, coords2):  # find distance between two coords
    # latitude is phi and longitude is theta relative to earth's center

    # converts spherical coordinates (lat & long) to cartesian, then uses distance formula
    # margin of error is +- .1 meters

    rho1 = coords1[2] + 6378100
    phi1 = coords1[0]
    theta1 = coords1[1]

    # cos & sin are swapped for cosphi/sinphi
    x1 = (
        rho1 * math.cos(phi1 * math.pi / 180) * math.cos(theta1 * math.pi / 180)
    )  # slightly off from typical conversion; idk why but it works
    y1 = (
        rho1 * math.cos(phi1 * math.pi / 180) * math.sin(theta1 * math.pi / 180)
    )  # slightly off from typical conversion; idk why but it works
    z1 = rho1 * math.sin(phi1 * math.pi / 180)  #

    rho2 = coords2[2] + 6378100
    phi2 = coords2[0]
    theta2 = coords2[1]

    # same deal as above
    x2 = rho2 * math.cos(phi2 * math.pi / 180) * math.cos(theta2 * math.pi / 180)
    y2 = rho2 * math.cos(phi2 * math.pi / 180) * math.sin(theta2 * math.pi / 180)
    z2 = rho2 * math.sin(phi2 * math.pi / 180)
    return math.sqrt(
        (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    )  # cartesian distance calculated


# return a properely initialized drone object, which acts as a way to interface with the pixhawk
async def connectToPixhawk():
    drone = System()
    await drone.connect(
        system_address="serial:///dev/serial0:57600"
    )  # tbh idk if this baudrate is correct but it works
    return drone


# takes in a initiliazed drone object and returns a list of booleans signaling if certain pre-flight requirements have been met
# check1 is making sure the pi is connected to the gopro AP ie SSID == "Hero10 Black"
# check2 is making sure the pixhawk is armed for flight
# check 3 is making sure we can ping the ground station
async def preFlightChecks(drone):
    check1 = None
    check2 = None
    check3 = None

    # check wi-fi ssid
    scanoutput = check_output(["iwlist", "wlan0", "scan"])
    ssid = "Wi-Fi not found"
    for line in scanoutput.split():
        line = line.decode("utf-8")
        if line[:5] == "ESSID":
            ssid = line.split('"')[1]
    print(ssid)
    check1 = ssid.startswith("HERO10")
    # check that the pi is connected to the pixhawk
    async for i in drone.telemetry.armed():
        check2 = i
        break

        # ping 192.168.1.1 (ground) for response
    try:

        pingGround = subprocess.check_output(["ping", "-c", "1", "192.168.1.1"])
        check3 = True
    except subprocess.CalledProcessError as e:
        check3 = False
        # ping('192.168.1.1', verbose=True)

        # return results
    if check1 and check2 and check3:
        print("Checks completed with no issues.")
    elif check1 and check2:
        print("Issue with pinging ground.")
    elif check1 and check3:
        print("Issue with connecting to pixhawk.")
    elif check2 and check3:
        print("Issue with wifi ssid.")
    elif check1:
        print("Issues with connecting to pixhawk and pinging ground.")
    elif check2:
        print("Issues with wifi ssid and pinging ground.")
    elif check3:
        print("Issues with wifi ssid and connecting to pixhawk.")
    else:
        print("All pre-flight checks failed.")
    return [check1, check2, check3]


# intialize sockets for sending gps and images utilizin socket connections
def initGPSSocket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, GpsPort))
    return client


def initImageSocket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, ImagePort))
    return client


def send_msg(sock: socket.socket, data_bytes: bytes):
    length = len(data_bytes)
    length_header = length.to_bytes(4, byteorder="big", signed=False)
    sock.sendall(length_header)
    sock.sendall(data_bytes)


# send image to ground station, with the specified sockets and bytes
def send_image(img_socket: socket.socket, gps_socket: socket.socket, data_bytes: bytes):
    while True:
        try:
            send_msg(img_socket, data_bytes)
            break
        except KeyboardInterrupt:
            print("interrupt")
            img_socket.shutdown(socket.SHUT_RDWR)
            gps_socket.shutdown(socket.SHUT_RDWR)
            img_socket.close()
            gps_socket.close()
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)
