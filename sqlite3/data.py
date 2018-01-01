# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:41:38 2017

@author: Administrator
"""
import pickle
ip="192.168.100.3"
f=open('para.txt','w')
pickle.dump(ip,f,0)
f.close()




