#this program connects to the gopro via bluetooth, enables the wireless ap and then creates an http get request for the cameras state. this is mainly a proof opf concept, and will eventually be modified to open a udp stream that
#we can use for cv.

#NOTES 
#should probably migrate to using subprocess library at some point, seems more robust than os
#The keep alive loop causes the gopro to get REALLY hot, so should look into cooling solutions
#find better way to do keep alive, as it seems super inefficient right now

#MUST RUN THIS WITH THIS COMMAND
#sudo -E python Connect_to_Gopro.py
#if you are getting a permission error its because you didnt use the command above

from open_gopro import WirelessGoPro
import open_gopro,os,time,requests

iface = input("enter wifi interface to use to connect to the gopro. if left empty, will default to wlan0")
if iface=="":
	iface = "wlan0"

gopro = WirelessGoPro(enable_wifi=False)
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


#keep-alive loop. prevents the gopro from falling asleep 

while(True):

	response = requests.get(url = "http://10.5.5.9:8080/gopro/camera/keep_alive" )
	time.sleep(3)
	print("sent keep-alive with status "+str(response.status_code))


"""
time.sleep(5)
command = "http://10.5.5.9:8080/gopro/camera/state"

r = requests.get(url=command)
data = r.json()

print(data)
"""
