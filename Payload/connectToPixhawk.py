import asyncio
from mavsdk import System


async def run():
	print("yuh")
	drone = System()
	print("yuh2")
	await drone.connect(system_address = "serial:///dev/serial0:57600")
	print("connected to pixhawk")
	initpos = (0,0,0)
	#pos = await drone.telemetry.position()
	async for position in drone.telemetry.position():
		latilogalt=position.split(",")
		print(position)
	

asyncio.run(run())
