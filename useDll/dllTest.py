# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 01:22:38 2018

@author: Administrator
"""
import cv2
from ctypes import *  
import datetime
import time
cam1=22386690
cam2=22386736

basler=CDLL('vision.dll')
basler.cap(1)
print(datetime.datetime.now())

    

basler.testIn(cam1)

  #  img = cv2.imread('bmpForProcess.bmp')
print(datetime.datetime.now())
#while(1):
#    cv2.imshow("img", img)    
#    cv2.waitKey(0)
#    break
#basler.testIn(cam1)
#print(datetime.datetime.now())
#basler.testIn(cam1)
#print(datetime.datetime.now())
#basler.testIn(cam1)
#print(datetime.datetime.now())


#e=basler.testOut()
##s=c_char()
###x=c_ubyte(55)
#s=pointer(x)	

#print(datetime.datetime.now())
#basler.cap(cam1)
#
##time.sleep(1)
#print(datetime.datetime.now())
#print(szbuffer)
#h=CDLL('usb2uis.dll')
#h.USBIO_GetVersion.argtypes=[c_ubyte,c_ubyte,c_char_p]
#cv2.Mat
