#TO BE TESTED
#this is supposed to be a refactor of the current codebase, for the purposes of centralizing everything
#goals of this file are centralization, implmenting multithreading/multiprocessing, have the main loop that will be running during flight


import requests,json,time,threading,os,socket
from PIL import Image
from io import BytesIO
import open_gopro
#globals
finished = False
ip = "http://10.5.5.9:8080"
def getImage():

	#set to photo mode
	command = "/gopro/camera/presets/set_group?id=1001"
	requests.get(url=ip+command)
	#take photo
	waitForCamera()
	command = "/gopro/camera/shutter/start"
	requests.get(url=ip+command)


        #waits for busy flag to be set to false
	print(waitForCamera())
	command = "/gopro/media/list"
	r = requests.get(url=ip+command)
	
	recent = r.json()["media"][0]["fs"][-1]["n"]
	
	command = "/videos/DCIM/100GOPRO/"+recent
	r = requests.get(url=ip+command)
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
        connected = os.system("nmcli dev wifi connect \"HERO10 Black\" password psY-mjc-Z+F ifname "+iface) 
        while connected == 2560: #2560 is the error code that is returned when nmcli cannot connect to the gopro, so this is essentially "while cannot find the gopro"
                print("retrying")
                time.sleep(5)
                os.system("sudo nmcli dev wifi rescan")
                connected = os.system("nmcli dev wifi connect \"HERO10 Black\" password psY-mjc-Z+F ifname "+iface)
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
        
def sendData(data):
	HOST = '192.168.1.1'
	PORT = 49161
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST,PORT))
	s.send(data)
	return s.recv(1024)
	

def main():
	connectToCamera("wlan0")
	data = getImage()
	sendData(data)

	finished = True

	
if __name__ == "__main__":
	main()
