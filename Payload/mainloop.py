import util
import asyncio
import socket
async def run():
    GPSSocket = util.initGPSSocket()
    ImageSocket = util.initImageSocket()
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
    async for cord in drone.telemetry.position():
        print("got a coordinate")
        currentCord = (cord.latitude_deg. cord.longitude_deg,cord.relative_altitude_m)
        distance = util.calcDistance(initialCord, currentCord)
        # if distance > 50:
        mangodog = input()
        if True:
            print("snap a pic and send")
            heading = None
            async for i in drone.telemetry.Heading():
                    heading = i
                    break
            print("got the last heading")
            gpsString = b""+id+","+currentCord[0]+","+currentCord[1]+","+currentCord[2]+","+heading
            GPSSocket.sendall(gpsString)
            id+=1
            ImageSocket.sendall(util.getImage())
asyncio.run(run())

