SHUTTER = 11
from gpiozero import Button
button = Button(17,pull_up = False)
while True:
	if button.is_pressed:
		print("image signal recieved")

