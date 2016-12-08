from flask import Flask, render_template, request
from PIL import Image
from subprocess import call
import sys

imgNum = 0
def fetch_new_image():

	call("/root/usb_cam/grabber.o")
	
	im = Image.open("/root/PepperPlant_Website/out001.ppm")
	
	tmp_name = '/root/PepperPlant_Website/static/webcam.jpg'

	im.save(tmp_name)

	call(["rm","/root/PepperPlant_Website/out000.ppm"\
		,"/root/PepperPlant_Website/out001.ppm"] )
	
app = Flask (__name__)

@app.route("/",methods=['GET','POST'])
def index ():
	if request.method == 'POST':
		requestType = request.form['requestType']
		print (requestType)
		fetch_new_image()
	return render_template("index.html")


if __name__ == "__main__":
	app.run(host = "0.0.0.0",debug = True)