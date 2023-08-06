import serial
from PIL import Image
#import IO
baud = 57600
bytesize = serial.EIGHTBITS
stopbits = serial.STOPBITS_ONE
paritybits = serial.PARITY_NONE
port =  "COM3"

bytelist =  []


ser = serial.Serial(port = port, baudrate = baud, bytesize = bytesize, stopbits = stopbits, parity = paritybits)
done = False
i = 0
while(done==False):
    
    bytelist[i] = ser.read(32)
    print(bytelist[i])
    

ser.close()

