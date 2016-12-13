
import time
import Adafruit_BBIO.GPIO as GPIO

# bluePin = "P9_12"
# redPin = "P9_15"

# LEDLightPin = "P9_23"
# GPIO.setup(LEDLightPin, GPIO.OUT)
# while (True):
# 	GPIO.output(LEDLightPin, GPIO.HIGH)
# 	print (GPIO.input(LEDLightPin))
# 	time.sleep(2)
# 	GPIO.output(LEDLightPin, GPIO.LOW)
# 	print (GPIO.input(LEDLightPin))
# 	time.sleep(2)
# GPIO.cleanup()


waterValvePin = "P9_15"
GPIO.setup(waterValvePin, GPIO.OUT)
# while (True):
GPIO.output(waterValvePin, GPIO.HIGH)
print (GPIO.input(waterValvePin))
time.sleep(10)
GPIO.output(waterValvePin, GPIO.LOW)
print (GPIO.input(waterValvePin))
	# time.sleep(2)
GPIO.cleanup()