#this program downloads the most recently taken image on the gopro over the gopros wifi connection. this program assumes the pi is already connected to the gopro, either manually or with Connect_to_Gopro.py
#should eventually incorporate the actual taking of the photos, with proper timing. also need to play around with stabilization settings, shutter speed, lenses, and turboTransfer


import requests
import json
from PIL import Image
from io import BytesIO

ip = "http://10.5.5.9:8080"
command = "/gopro/media/list"

r = requests.get(url=ip+command)
recent = ""
#this loop serves two purposes, it allowed me to see the structure of the json file, and sets recent to the filename of the most recent photo/video taken
#this loop should be removed in the future, as it has served its purpose
for d in r.json()["media"]: #loops through every directory on the sd card
	print(d["d"]) #print directory name
	for file in d["fs"]: #for every file in the directory
		print(j)
		recent = file["n"] #n is the filename tag

command = "/videos/DCIM/100GOPRO/"+file
r = requests.get(url=ip+command)
#print(r.encoding)
#print(r.content)
i = Image.open(BytesIO(r.content))
i.save("recent.jpg")
