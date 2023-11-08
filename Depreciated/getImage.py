#this program downloads the most recently taken image on the gopro over the gopros wifi connection. this program assumes the pi is already connected to the gopro, either manually or with Connect_to_Gopro.py
#should eventually incorporate the actual taking of the photos, with proper timing. also need to play around with stabilization settings, shutter speed, lenses, and turboTransfer
#need to implement is_busy check before we send commands to the gopro, as just using a raw time.sleep is unreliable

import requests
import json
from PIL import Image
from io import BytesIO
import time
ip = "http://10.5.5.9:8080"
def getImage():
	
	command = "/gopro/camera/shutter/start"
	requests.get(url=ip+command)


	
	print(waitForCamera())
	
	r = requests.get(ip+"/gopro/media/list")
	recent = r.json()["media"][0]["fs"][-1]["n"]

	command = "/videos/DCIM/100GOPRO/"+recent
	r = requests.get(url=ip+command)
	print(type(r.content))
	#i = BytesIO(r.content)
	return r.content
	
def waitForCamera():
	command = "/gopro/media/list"

        r = requests.get(url=ip+command)
        busytime = 0
        while len(r.json().keys()) == 1:
                time.sleep(0.1)
                r = requests.get(url=ip+command)
                busytime += 0.1
	return busytime
def photoMode():
	command = 


