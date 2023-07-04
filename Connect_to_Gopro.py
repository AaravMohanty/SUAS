#this program connects to the gopro via bluetooth, enables the wireless ap and then creates an http get request for the cameras state. this is mainly a proof opf concept, and will eventually be modified to open a udp stream that
#we can use for cv. 



from open_gopro import WirelessGoPro
import open_gopro,os,time,requests

gopro = WirelessGoPro(enable_wifi=False)
gopro.open()

print("connected")
gopro.ble_command.enable_wifi_ap(enable=True)

print("wifi enabled")

gopro.close()
print("connection closed")
time.sleep(10)

#program seems to fail here completely randomly, with it being able to connect to the gopro around 50% of the time. running it again seems to fix it tho so 
#should change this to wait until nmcli sees the gopro before connecting
os.system("nmcli dev wifi connect \"HERO10 Black\" password psY-mjc-Z+F")
time.sleep(5)
command = "http://10.5.5.9:8080/gopro/camera/state"

r = requests.get(url=command)
data = r.json()

print(data)

