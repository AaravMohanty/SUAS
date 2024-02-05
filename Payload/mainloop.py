import util
import asyncio

async def run():
	drone =  await util.connectToPixhawk()
	util.connectToCamera("wlan0")
	await util.preFlightChecks(drone)
asyncio.run(run())

