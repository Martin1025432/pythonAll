# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:22:29 2017

@author: Administrator
"""

import cv2
import numpy as np
img = cv2.imread('test0.jpeg')

moments = cv2.moments(img)
hu_moments = cv2.HuMoments(img)
moment=[i+10 for i in range(10)]
print(moment)
