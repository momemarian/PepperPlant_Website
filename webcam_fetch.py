from PIL import Image
from subprocess import call
# def fetch_image ():

call("/root/usb_cam/grabber.o")
im = Image.open('/root/usb_cam/out001.ppm')
im.save("/root/PepperPlant_Website/static/webcam.jpg")
# call(["rm","/root/PepperPlant_Website/out000.ppm"\
# 	,"/root/PepperPlant_Website/out001.ppm"] )