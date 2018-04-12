# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 21:28:45 2018

@author: Administrator
"""
from serial import *
#from __future__ import division
#import sys
#import cv2
#from PyQt5 import QtCore, QtWidgets, uic
#from PyQt5.QtGui import QPixmap


def calCRC(inStr):
    a=[i for i in inStr]
#    a=['@','0','0','W','D','0','1','0','0','0','0','0','1']
    b=[ord(i) for i in a]
    c=[dl&0x0f for dl in b ]
    d=[dh>>4 for dh in b]
    result=c[0]
    for i in range(1,len(c)):
        result=result^c[i]
    print(result)
    result2=d[0]
    for i in range(1,len(d)):
        result2=result2^d[i]
    print(result2)   
    return result2,result
#ser = serial.Serial(1, 38400, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
def openSerial():
    global ser
    ser = Serial(  
    port="COM4",              # number of device, numbering starts at  
# zero. if everything fails, the user  
# can specify a device string, note  
# that this isn't portable anymore  
# if no port is specified an unconfigured  
# an closed serial port object is created  
    baudrate=9600,          # baud rate  
    bytesize=EIGHTBITS,     # number of databits  
    parity=PARITY_NONE,     # enable parity checking  
    stopbits=STOPBITS_ONE,  # number of stopbits  
    timeout=None,           # set a timeout value, None for waiting forever  
    xonxoff=0,              # enable software flow control  
    rtscts=0,               # enable RTS/CTS flow control  
    interCharTimeout=None   # Inter-character timeout, None to disable  
    )  
global ser
#ser.close()
in0="@00WR00030004"
H,L=calCRC(in0)
#out0=in0+str(H)+str(L)+"*\#13\#10"
out0=in0+str(H)+str(L)+"*"+'\r'+'\n'

openSerial()
ser.write(bytes(out0,encoding='utf-8')) 
s = ser.read(10)        # read up to ten bytes (timeout)  
print(s)
ser.close()

#line = ser.readline()   # read a '\n' terminated line  
#ser.close()  
#in0="@00RD01000001"
#in1=int0+str(result2)+str(result)
