# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 01:22:38 2018

@author: Administrator
"""
import cv2
from ctypes import *  
import datetime
import time



h=CDLL('vision.dll')
time.sleep(2)
#s=c_char()
##x=c_ubyte(55)
##s=pointer(x)	

print(datetime.datetime.now())
h.grabt()
#time.sleep(1)
print(datetime.datetime.now())
#print(szbuffer)
#h=CDLL('usb2uis.dll')
#h.USBIO_GetVersion.argtypes=[c_ubyte,c_ubyte,c_char_p]
#cv2.Mat
