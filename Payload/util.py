#TO BE TESTED
#this is supposed to be a refactor of the current codebase, for the purposes of centralizing everything
#goals of this file are centralization, implmenting multithreading/multiprocessing, have the main loop that will be running during flight


#imports
import requests,json,time,threading,os,subprocess,math
from open_gopro import WirelessGoPro
from PIL import Image
import math
import asyncio
from mavsdk import System 
from subprocess import check_output
from pythonping import ping

#globals
finished = False
ip = "http://10.5.5.9:8080"

def getImage():
    #set to photo mode
	command = "/gopro/camera/set_group?1d=1001"
	requests.get(url=ip+command)
	#take photo
	command = "/gopro/camera/shutter/start"
	requests.get(url=ip+command)


    #waits for busy flag to be set to false
	waitForCamera()
             
	command = "/gopro/camera/list"                 
	r = requests.get(url=ip+command)

	recent = r.json()["media"][0]["fs"][-1]["n"]

	command = "/videos/DCIM/100GOPRO/"+recent
	r = requests.get(url=ip+command)
	print(type(r.content))
	#i = BytesIO(r.content)
	return r.content

def waitForCamera():

	command = "/gopro/camera/state"
	busytime = 0
	response = requests.get(url=ip+command) 
	while response.json()["status"]["8"] == 1:
		time.sleep(0.1)
		busytime+=0.1
		response = requests.get(url=ip+command)
	return busytime

def connectToCamera(iface):
        #if iface=="":
        #       iface = "wlan0"

	gopro =open_gopro.WirelessGoPro(enable_wifi=False)
	print("opening GoPro Bluetooth connection..")
	gopro.open()

	print("connected")
	gopro.ble_command.enable_wifi_ap(enable=True)

	print("wifi AP enabled")

	gopro.close()
	print("Bluetooth connection closed")


	os.system("sudo nmcli dev wifi rescan")
	connected = os.system("nmcli dev wifi connect \"HERO10 Black\" password psY-mjc-Z+F ifname "+ iface)
	while connected == 2560: #2560 is the error code that is returned when nmcli cannot connect to the gopro, so this is essentially "while cannot find the gopro"
		print("retrying")
		time.sleep(5)
		os.system("sudo nmcli dev wifi rescan")
		connected = os.system("nmcli dev wifi connect \"HERO10 Black\" password psY-mjc-Z+F ifname "+ iface)
                #this loop usually takes around 2-4 tries to find it, so dont freak out if it cant find it immediately

	keepAliveThread = threading.Thread(target = keepAlive, args = (60,), daemon = True )
	keepAliveThread.start()
        #keepAliveThread.join()

def keepAlive(interval):
        while(True):
                response = requests.get(url = "http://10.5.5.9:8080/gopro/camera/keep_alive" )
                time.sleep(interval)
                print("sent keep-alive with status "+str(response.status_code))
                if finished:
                        break

def main():
	connectToCamera("wlan0")
	data = getImage()

if __name__ == "__main__":
	main()
        
def projectOntoPlane(lang,long):
        rho = 3,958.8
        x = rho * math.sin(long) * math.cos(lang)
        y = rho * math.sin(long) * math.sin(lang)
        
        r = math.sqrt(x**2 + y**2)
        theta = math.atan(y/x)
        return (r,theta)

def calcDistance(coords1, coords2): # find distance between two coords
# latitude is phi and longitude is theta relative to earth's center

# converts spherical coordinates (lat & long) to cartesian, then uses distance formula
# margin of error is +- .1 meters
    
    rho1 = coords1[2] + 6378100
    phi1 = coords1[0]
    theta1 = coords1[1]

    # cos & sin are swapped for cosphi/sinphi
    x1 = rho1*math.cos(phi1*math.pi/180)*math.cos(theta1*math.pi/180) # slightly off from typical conversion; idk why but it works
    y1 = rho1*math.cos(phi1*math.pi/180)*math.sin(theta1*math.pi/180) # slightly off from typical conversion; idk why but it works
    z1 = rho1*math.sin(phi1*math.pi/180) #

    rho2 = coords2[2] + 6378100
    phi2 = coords2[0]
    theta2 = coords2[1]

    #same deal as above
    x2 = rho2*math.cos(phi2*math.pi/180)*math.cos(theta2*math.pi/180)
    y2 = rho2*math.cos(phi2*math.pi/180)*math.sin(theta2*math.pi/180)
    z2 = rho2*math.sin(phi2*math.pi/180)
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) # cartesian distance calculated

def connectToPixhawk():
       async def run():
              drone = System()
              await drone.connect(system_address = "serial:///dev/serial0:57600")
              initialPosition=(0,0,0)
              async for position in drone.telemetry.position():
                     currentPosition = (position.latitude_deg, position.longitude_deg, position.relative_altitude_m)
                     distance = calcDistance (initialPosition, currentPosition)
                     if distance > 50:
                        print("image trigger")

def preFlightChecks():
       #check wi-fi ssid
       scanoutput = check_output(["iwlist","wlan0",'scan'])
       ssid = "Wi-Fi not found"
       for line in scanoutput.split():
              line = line.decode("utf-8")
              if line[:5] == "ESSID":
                     ssid = line.split('"')[1]
        print(ssid)
       
       #check that the pi is connected to the pixhawk
       #drone.telemetry.Telemetry
       armed = drone.telemetry.Telemetry(armed)
       print(armed)

       #ping 192.168.1.1 (ground) for response
       ping('192.168.1.1', verbose=True)
