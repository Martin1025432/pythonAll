# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 21:14:40 2018

@author: Administrator
"""

import datetime
import time
import numpy as np
import cv2
#from findEdge import *
print(datetime.datetime.now())
cap = cv2.VideoCapture(0)

#相机像索设置
w=2592
h=1944
cap.set(3,w)   
cap.set(4,h)  
print(datetime.datetime.now())