from subprocess import Popen,TimeoutExpired,PIPE, call
import datetime, time
import threading
from os.path import getctime
import os
import glob



call(["rm","-r", "./test"])
call(["mkdir","test"])
i = 1


def fetch_new_image_periodic(i):

    print (i)
    currTime = datetime.datetime.now()
    imgFileName = 'imagePeriodic_{0}.jpg'.format(currTime.strftime("%y_%m_%d_%H_%M_%S"))
    webSiteRoot = os.getcwd()
    webcamProc = Popen (["{0}/v4l2grab/v4l2grab".format(webSiteRoot), 
        "-W", "1920", "-H", "1080", "-q", "100"
        , "-o", '{0}/test/{1}'.format(webSiteRoot,imgFileName)], stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = webcamProc.communicate(timeout=10)
        print ("ERRORS: {0} \nOUTPUT: {1}".format(errs,outs))
        if errs == b'':
            print ("Grabbed the periodic frame {0}\n".format(imgFileName))
            i += 1
            threading.Timer(30, fetch_new_image_periodic,args = [i]).start()  
        else:
            print ("Video Buffer Error")
            threading.Timer(5, fetch_new_image_periodic,args = [i]).start()  
    except TimeoutExpired:
        webcamProc.kill()
        outs, errs = webcamProc.communicate()
        print ("ERRORS: {0} \nOUTPUT: {1}".format(errs,outs))
        print ("Timed out")
        threading.Timer(5, fetch_new_image_periodic,args = [i]).start()  
    
def find_lates_image ():
    
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

       
print (find_lates_image())


# fetch_new_image_periodic(i)