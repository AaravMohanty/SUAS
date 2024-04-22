import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)

pin = 16
GPIO.setup(16,GPIO.OUT)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)

def servoangle(ang):
    angle = 2.5 + (ang/18)
    pwm.ChangeDutyCycle(angle)
    time.sleep(0.05)

#range = vel*math.sqrt(2*height/9.8) + vel*#servoTime
#if((range + 2) < distance):
for open in range(0, 91, 10):
    servoangle(open)
    
for close in range(91, 0, 10):
    servoangle(close)
