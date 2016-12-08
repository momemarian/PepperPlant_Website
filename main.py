from flask import Flask, render_template, request
from PIL import Image
from subprocess import call
import sys

imgNum = 0
def fetch_new_image():

	imgNumber = 1

	call("/root/usb_cam/grabber.o")
	
	im = Image.open("/root/PepperPlant_Website/out001.ppm")
	
	tmp_name = '/root/PepperPlant_Website/static/webcam_{0:d}.jpg'.format(imgNumber)

	im.save(tmp_name)

	call(["rm","/root/PepperPlant_Website/out000.ppm"\
		,"/root/PepperPlant_Website/out001.ppm"] )

	return imgNumber
	
app = Flask (__name__)

@app.route("/",methods=['GET','POST'])
def index ():
	if request.method == 'POST':
		requestType = request.form['requestType']
		if requestType == "RefreshImage":
			return str(fetch_new_image())

	imgNumber = str(fetch_new_image())
	return render_template("index.html",imgNumber=imgNumber)


if __name__ == "__main__":
	app.run(host = "0.0.0.0",debug = True,threaded=True)