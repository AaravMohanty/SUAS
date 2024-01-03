import asyncio
from mavsdk import System


async def run():
	print("yuh")
	drone = System()
	print("yuh2")
	await drone.connect(system_address = "serial:///dev/ttyS0:57600")
	print("connected to pixhawk")

	all_params = await drone.param.get_all_params()
	for param in all_params.int_params:
		print(f"{param.name}: {param.value}")
	print("collected all params")

asyncio.run(run())
