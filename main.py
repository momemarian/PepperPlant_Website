from flask import Flask, render_template, request
from PIL import Image
from subprocess import call
import sys
from os import listdir
from os.path import isfile, join
import os
import datetime


def find_lates_image ():
    
    imageDir = os.getcwd() + "/static/webcam_images"
    imageFiles = listdir(imageDir)
    
    return max(imageFiles)
def fetch_new_image():

    currTimeStamp = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    # latestImage = find_lates_image()
    
    # print (latestImage)

    imgFileName = 'webcam_{0}.jpg'.format(currTimeStamp)
    webSiteRoot = "/root/PepperPlant_Website/"
    
    call("/root/usb_cam/grabber.o")

    im = Image.open(webSiteRoot+"out001.ppm")    
    im.save('{0}static/webcam_images/{1}'.format(webSiteRoot,imgFileName))

    call(["rm",webSiteRoot+"out000.ppm"\
        ,webSiteRoot+"out001.ppm"] )


    return imgFileName
    
app = Flask (__name__)

@app.route("/",methods=['GET','POST'])
def index ():
    if request.method == 'POST':
        requestType = request.form['requestType']
        if requestType == "RefreshImage":
            return fetch_new_image()

    imgFileName = fetch_new_image()
    return render_template("index.html",imgFileName=imgFileName)


if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug = True,threaded=True)