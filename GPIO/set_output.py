
import time
import Adafruit_BBIO.GPIO as GPIO

# bluePin = "P9_12"
# redPin = "P9_15"

LEDLight = "P9_23"
GPIO.setup(LEDLight, GPIO.OUT)
while (True):
	GPIO.output(LEDLight, GPIO.HIGH)
	print (GPIO.input(LEDLight))
	time.sleep(2)
	GPIO.output(LEDLight, GPIO.LOW)
	print (GPIO.input(LEDLight))
	time.sleep(2)
GPIO.cleanup()

