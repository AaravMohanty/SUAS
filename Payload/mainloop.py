import util
import asyncio
import socket
async def run():
	GPSSocket = util.initGPSSocket()
	ImageSocket = util.initImageSocket()
	drone =  await util.connectToPixhawk()
	#util.connectToCamera("wlan0")
	checks = await util.preFlightChecks(drone)
	if checks[2] = False:
		util.connectToCamera("wlan0")
	initialCord = (0,0,0)
	id = 0
	await for cord in drone.telemetry.Position():
		currentCord = (cord.latitude_deg. cord.longitude_deg,cord.relative_altitude_m)
		distance = util.calcDistance(initialCord, currentCord)
		if distance > 50:
			heading = None
			await for i in dron.telemetry.Heading():
				heading = i
				break
			gpsString = b""+id+","+currentCord[0]+","+currentCord[1]+","+currentCord[2]+","+heading
			GPSSocket.sendall(gpsString)
			id+=1
			ImageSocket.sendall(util.getImage())
asyncio.run(run())

