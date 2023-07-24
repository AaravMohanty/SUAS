import serial
import io
from getImage import getImage

#CONTSANTS

baud = 57600
bytesize = serial.EIGHTBITS
stopbits = serial.STOPBITS_ONE
paritybits = serial.PARITY_NONE
port =  "/dev/ttyUSB0"

ser = serial.Serial(port = port, baudrate = baud, bytesize = bytesize, stopbits = stopbits, parity = paritybits)

ser.write(getImage())

ser.close()


