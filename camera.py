# Script taken from:
#https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/sdsd
# Before starting script: sudo raspi-config -> Enable Camera -> Reboot Rasperry
from picamera import PiCamera
from time import sleep, localtime, strftime

print("Starting Camera Module")

camera = PiCamera()
camera.rotation = 0               # To turn camera picture by 180deg
camera.start_preview()
camera.annotate_text = strftime("%d.%m.%Y %H:%M:%S", localtime())
camera.resolution = (500, 500) #To find default resolution (that of your screen), enter in shell:$ xdpyinfo | grep "dimensions" | awk '{ print $2 }'
camera.annotate_text_size = 12

sleep(5)                             # 2 sec min sleep time required for camera to adjust light level 
folderLocationName="/home/pi/BioMaker/GitHubGardenObserver/Data/"

dateAndTimeInOneNumber=strftime("%Y%m%d_%H%M%S", localtime())
camera.capture(folderLocationName+'GardenPiCam_'+dateAndTimeInOneNumber+'.jpg')


###Test CameraFilters
##for filterNames in camera.IMAGE_EFFECTS:
##    sleep(0.01) 
##    camera.image_effect = filterNames
##    camera.annotate_text= filterNames
##    camera.capture(folderLocationName+'GardenPiCam_'+filterNames+dateAndTimeInOneNumber+'.jpg')

###Test CameraAutoBlackWhiteMode
##for awbMode in camera.AWB_MODES:
##    sleep(0.01) 
##    camera.awb_mode = awbMode
##    camera.annotate_text= awbMode
##    camera.capture(folderLocationName+'GardenPiCam_'+awbMode+dateAndTimeInOneNumber+'.jpg')

###Test CameraExposureMode
##for exposureMode in camera.EXPOSURE_MODES:
##    sleep(0.01) 
##    camera.exposure_mode = exposureMode
##    camera.annotate_text= exposureMode
##    camera.capture(folderLocationName+'GardenPiCam_'+exposureMode+dateAndTimeInOneNumber+'.jpg')


camera.stop_preview()
