import asyncio
from mavsdk import System
import calcDistance
from subprocess import check_output

#async def run():
	#print("yuh")
	#drone = System()
	#print("yuh2")
	#await drone.connect(system_address = "serial:///dev/serial0:57600")
	#print("connected to pixhawk")
	#initialPosition = (0,0,0)
	##pos = await drone.telemetry.position()
	#async for position in drone.telemetry.position():
		#currentPosition = (position.latitude_deg,position.longitude_deg, position.relative_altitude_m)
		#distance = calcDistance(initialPosition,currentPosition)
		#if distance > 50:
			#print("image trigger")

#asyncio.run(run())

scanoutput = check_output(["iwlist", "wlan0", "scan"])
ssid = "WiFi not found"
for line in scanoutput.split():
	line = line.decode("utf-8")
	if line[:5] =="ESSID":
		ssid = line.split('"')[1]
print(ssid)
