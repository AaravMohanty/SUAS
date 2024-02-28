import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)

pin = 10
GPIO.setup(11,GPIO.OUT)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)

def servoangle(ang):
    angle = 2.5 + (ang/18)
    pmw.ChangeDutyCycle(angle)
    time.sleep(0.10)

#range = vel*math.sqrt(2*height/9.8) + vel*#servoTime
#if((range + 2) < distance):
    for open in range(0, 91, 10):
        servoangle(open)
    
    for close in range(91, 0, 10):
        servoangle(close)
