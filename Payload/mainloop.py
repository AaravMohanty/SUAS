import util
import asyncio
import socket
async def run():
    gps_socket = util.initGPSSocket()
    img_socket = util.initImageSocket()
    print("gps and image socket initialized, connecting to pixhawk...")
    drone =  await util.connectToPixhawk()
    print("connected to pixhawk")
    #util.connectToCamera("wlan0")
    print("running pre flight checks...")
    checks = await util.preFlightChecks(drone)
    print("pre flight checks complete")
    if not checks[0]: # whether we're connected to the camera's WiFi SSID
        print("connecting to camera...")
        util.connectToCamera("wlan0")
    initialCord = (0,0,0)
    id = 0
    print("about to get some coords from the pixhawk:")
    async for coord in drone.telemetry.position():
        print("got a coordinate")
        currentCord = (coord.latitude_deg, coord.longitude_deg,coord.relative_altitude_m)
        distance = util.calcDistance(initialCord, currentCord)
        # if distance > 50:
        mangodog = input()
        if True:
            print("snap a pic and send")
            heading = None
            async for i in drone.telemetry.heading():
                    heading = i.heading_deg
                    break
            print("got the last heading")
            gps_data = util.GPSData(id, currentCord[0], currentCord[1],currentCord[2],heading)
            gps_socket.sendall(gps_data.into_socket_msg())
            id+=1
            util.send_image(img_socket, gps_socket, util.getImage())
asyncio.run(run())

