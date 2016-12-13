from flask import Flask, render_template, request
from subprocess import Popen,TimeoutExpired,PIPE, call
import Adafruit_BBIO.GPIO as GPIO
from os.path import getctime
import os
import glob
import datetime, time
import threading


webcamLock = threading.Lock()

def find_image (imageSrc,requestType = 'next'):
    
    imgFiles = glob.iglob('./static/webcam_images/*.jpg')
    imageFiles = sorted(imgFiles)
    clienImageName = imageSrc.split("/")[-1]
    preImageName = clienImageName
    for i,imageFile in  enumerate(imageFiles):
        serverImageName = imageFile.split("/")[-1]
        if clienImageName == serverImageName:
            if requestType == 'next':
                if i < len(imageFiles) -2 :
                    return imageFiles[i+1].split("/")[-1]
                else:
                    return clienImageName
            elif requestType == 'pre':
                if 1 < i  :
                    return imageFiles[i-1].split("/")[-1]
                else:
                    return clienImageName 
    return clienImageName


def find_latest_image ():
    
    imageFiles = glob.iglob('./static/webcam_images/*.jpg')
    try:
        latestImageName = max(imageFiles, key=os.path.getctime)
        latestImageName = latestImageName.split("/")[-1]
        tmpStr = latestImageName.split(".")[0]
        tmpStr = tmpStr.split("_")
        latestImageTime = datetime.datetime(2000+int(tmpStr[1]), int(tmpStr[2]), int(tmpStr[3]), int(tmpStr[4]), int(tmpStr[5]),int(tmpStr[6]))
        return latestImageTime,latestImageName
    except ValueError:
        return datetime.datetime(2016, 12, 9, 0, 0,0),""


def fetch_new_image():

    webcamAccess = webcamLock.acquire(False)

    if webcamAccess:
        print ("Requesting an image from the webcam.")
        currTime = datetime.datetime.now()
        imgFileName = 'image_{0}.jpg'.format(currTime.strftime("%y_%m_%d_%H_%M_%S"))
        webSiteRoot = os.getcwd()
        webcamProc = Popen (["{0}/v4l2grab/v4l2grab".format(webSiteRoot), 
            "-W", "1920", "-H", "1080", "-q", "100"
            , "-o", '{0}/static/webcam_images/{1}'.format(webSiteRoot,imgFileName)], stdout=PIPE, stderr=PIPE)
        try:
            outs, errs = webcamProc.communicate(timeout=10)
            if errs == b'':
                print ("Received the requested image {0}.\n".format(imgFileName))
                webcamLock.release()
                return imgFileName
            else:
                print ("ERROR: VIDEO BUFFER")
                webcamLock.release()
                time.sleep(5) 
                return fetch_new_image()
        except TimeoutExpired:
            webcamProc.kill()
            outs, errs = webcamProc.communicate()
            print ("ERROR: TIME OUT")
            webcamLock.release()
            time.sleep(5)
            return fetch_new_image()
    else:
        print ("The webcam is busy.")
        return "",400 # http error code 


def fetch_new_image_periodic(periodInSeconds):

    currTime = datetime.datetime.now()
    latestImageTime,latestImageName = find_latest_image()
    timeDiff = (currTime-latestImageTime).total_seconds()

    if timeDiff > periodInSeconds:
        print ("Periodic Imaging.")
        fetch_new_image()
    else:
        print ("Already Taken an image within the last {} seconds.".format(periodInSeconds))
    
    threading.Timer(periodInSeconds, fetch_new_image_periodic, args=[periodInSeconds]).start()
        
 


app = Flask (__name__)
@app.route("/",methods=['GET','POST'])
def index ():
    if request.method == 'POST':
        requestType = request.form['requestType']
        if requestType == "RefreshImage":
            return fetch_new_image()
        if requestType == "LastImage":
            latestImageTime,latestImageName = find_latest_image()
            return latestImageName
        if requestType == "PreImage":
            imageName = request.form['imageName']
            preImageName = find_image(imageName, requestType = 'pre')
            return preImageName
        if requestType == "NextImage":
            imageName = request.form['imageName']
            preImageName = find_image(imageName, requestType = 'next')
            return preImageName
        if requestType == "LEDStatus":
            LEDStatus = GPIO.input(LEDLight)
            if LEDStatus:
                return "ON"
            else:
                return "OFF"
        if requestType == "LEDToggle":
            LEDStatus = GPIO.input(LEDLight)
            print (LEDStatus)
            if LEDStatus:
                GPIO.output(LEDLight, GPIO.LOW)
            else:
                GPIO.output(LEDLight, GPIO.HIGH)

    latestImageTime,latestImageName = find_latest_image()
    return render_template("index.html",imgFileName=latestImageName)


if __name__ == "__main__":
    LEDLight = "P9_23"
    GPIO.setup(LEDLight, GPIO.OUT)
    GPIO.output(LEDLight, GPIO.LOW)
    # fetch_new_image_periodic(300)
    app.run(host = "0.0.0.0",threaded=True)
# ,debug=True

