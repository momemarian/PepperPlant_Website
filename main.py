from flask import Flask, render_template, request
from PIL import Image
from subprocess import call
import sys
from os import listdir
from os.path import isfile, join
import os
import datetime, time


def find_lates_image ():
    
    imageDir = os.getcwd() + "/static/webcam_images"
    imageFiles = listdir(imageDir)
    latestImage = max(imageFiles)

    tmpStr = latestImage.split(".")[0]
    tmpStr = tmpStr.split("_")
    latestImageTime = datetime.datetime(2000+int(tmpStr[1]), int(tmpStr[2]), int(tmpStr[3]), int(tmpStr[4]), int(tmpStr[5]),int(tmpStr[6]))
    return latestImageTime

def fetch_new_image():

    currTime = datetime.datetime.now()
    latestImageTime = find_lates_image()
    timeDiff = (currTime-latestImageTime).total_seconds()

    if (timeDiff > 10.0):
        imgFileName = 'webcam_{0}.jpg'.format(currTime.strftime("%y_%m_%d_%H_%M_%S"))
        webSiteRoot = os.getcwd()
        call(["{0}/v4l2grab/v4l2grab".format(webSiteRoot), "-W", "1920", "-H", "1080", "-q", "100", "-o", '{0}/static/webcam_images/{1}'.format(webSiteRoot,imgFileName)])
        print ("Grabbing a new frame")    
    else:
        imgFileName = 'webcam_{0}.jpg'.format(latestImageTime.strftime("%y_%m_%d_%H_%M_%S")) 
        print ("Too quick")
    return imgFileName

app = Flask (__name__)
@app.route("/",methods=['GET','POST'])
def index ():
    if request.method == 'POST':
        requestType = request.form['requestType']
        if requestType == "RefreshImage":
            return fetch_new_image()
            # return '0'

    imgFileName = fetch_new_image()
    # imgFileName = '0'
    return render_template("index.html",imgFileName=imgFileName)


if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug = True,threaded=True)