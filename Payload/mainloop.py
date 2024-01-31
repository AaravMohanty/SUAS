import util
import asyncio

async def run():
	drone =  await util.connectToPixhawk()
	await util.preFlightChecks(drone)
asyncio.run(run())

