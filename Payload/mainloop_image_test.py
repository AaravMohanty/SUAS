import time
import util
import asyncio
import socket


async def run():
    gps_socket = util.initGPSSocket()
    img_socket = util.initImageSocket()
    print("gps and image socket initialized, connecting to pixhawk...")
    drone = await util.connectToPixhawk()
    print("connected to pixhawk")
    # util.connectToCamera("wlan0")
    print("running pre flight checks...")
    checks = await util.preFlightChecks(drone)
    print("pre flight checks complete")
    if not checks[0]:  # whether we're connected to the camera's WiFi SSID
        print("connecting to camera...")
        util.connectToCamera("wlan0")
    for id in range(0, 3):
        gps_data = util.GPSData(id, 0, 0, 0, 0)
        print("sending fake GPS coordinate...")
        util.send_msg(gps_socket, gps_data.into_socket_msg())
        print("taking picture...")
        gopro_img = util.getImage()
        print("sending image with size " + str(len(gopro_img)) + "...")
        util.send_image(img_socket, gps_socket, gopro_img)
        print("image sent. waiting 2 seconds...")
        time.sleep(2)

asyncio.run(run())
