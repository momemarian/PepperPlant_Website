from flask import Flask, render_template, request
from PIL import Image
from subprocess import call
import sys

imgNum = 0
def fetch_new_image():

	webSiteRoot = "/root/PepperPlant_Website/"
	imgNumber = 1

	call("/root/usb_cam/grabber.o")
	
	im = Image.open(webSiteRoot+"out001.ppm")
	
	tmp_name = '{0}static/webcam_{1:d}.jpg'.format(webSiteRoot,imgNumber)

	im.save(tmp_name)

	call(["rm",webSiteRoot+"out000.ppm"\
	 	,webSiteRoot+"out001.ppm"] )

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