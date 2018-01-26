# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:32:50 2018

@author: Administrator
"""
import datetime
import time

s1=time.time()
#s1=int(s1.microsecond)/1000000
time.sleep(1/10)
s2=time.time()
#
#c=((s2-s1).minute*60000000+(s2-s1).seconds*1000000+(int(s2.microsecond)-int(s1.microsecond)))/1000000
##s2=int(s2.microsecond)/1000000
print(s2-s1)
  