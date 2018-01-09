# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 12:00:54 2018

@author: Administrator
"""

from multiprocessing import Pool
import os, time, random
import threading
class pro():
def long_time_task(f):
    print(f)
    
def kk(g):
    print(g)
    name='dd'
    t1 = threading.Thread(target=long_time_task,args=(name,))
    t1.start()
name='gg'
t2 = threading.Thread(target=kk,args=(name,))
t2.start()