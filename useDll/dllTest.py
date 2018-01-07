# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 01:22:38 2018

@author: Administrator
"""
import cv2
from ctypes import *  
import datetime
import time
cam1="22386690"
cam2="22386736"
sn=[]
basler=CDLL('vision.dll')
basler.capIni()
#获取相机序列号
#for i in range(0,4):  
#    sizebuffer=basler.outputStr(i)
#    print(c_char_p(sizebuffer).value)
#    recStr=str(c_char_p(sizebuffer).value)[2:-1]
#    sn.append(recStr)
#for i in range(5):
#    print(datetime.datetime.now())
#    basler.capBmp(sn.index(cam1))

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
