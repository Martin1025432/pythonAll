# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 11:22:18 2018

@author: Administrator
"""

from serial import *
#from __future__ import division
import sys

#def __init__():
#    
#    global d100,d101,d102,d103,d104,d105,d106,d107,d108,d109,d110,com     
#    com=openSerial()
#    readAll()
    
def readAll():
    global d100,d101,d102,d103,d104,d105,d106,d107,d108,d109,d110   
    d100=read("100")
    d101=read("101")   
    d102=read("102")
    d103=read("103")     
    d104=read("104")
    d105=read("105")     
    d106=read("106")
    d107=read("107") 
    d108=read("108")
    d109=read("109") 
    d110=read("110")


    
def on(data,bit):
    global com
    global d100,d101,d102,d103,d104,d105,d106,d107,d108,d109,d110  
    D={"100":d100,"101":d101,"102":d102,"103":d103,"104":d104,"105":d105,\
       "106":d106,"107":d107,"108":d108,"109":d109,"110":d110}
    a=[1<<i for i in range(0,16)]
    dataValue=read(data)
    dataOut=dataValue|a[bit]
    print(dataOut,hex(dataOut),hex(dataOut)[2:len(hex(dataOut))])
    write(data,hex(dataOut)[2:len(hex(dataOut))])
    
    return dataOut

def off(data,bit):
    global com
    global d100,d101,d102,d103,d104,d105,d106,d107,d108,d109,d110   
    a=[1<<i for i in range(0,16)]
    b=[0xffff^aValue for aValue in a]
    dataValue=read(data)
    dataOut=dataValue&b[bit]
    write(data,hex(dataOut)[2:len(hex(dataOut))])
    return dataOut

def openSerial():
    global com
    com = Serial(  
    port="COM10",              # number of device, numbering starts at   
    baudrate=115200,          # baud rate  
    bytesize=EIGHTBITS,     # number of databits  
    parity=PARITY_NONE,     # enable parity checking  
    stopbits=STOPBITS_ONE,  # number of stopbits  
    timeout=0.1,           # set a timeout value, None for waiting forever  
    xonxoff=0,              # enable software flow control  
    rtscts=0,               # enable RTS/CTS flow control  
    interCharTimeout=None   # Inter-character timeout, None to disable      
    )
    return com

def calCRC(inStr):
    a=[i for i in inStr]

    b=[ord(i) for i in a]
    c=[dl&0x0f for dl in b ]
    d=[dh>>4 for dh in b]
    print(b,c)
    result=c[0]
    
    for i in range(1,len(c)):
        result=result^c[i]
       # print(result)
        result2=d[0]
    for ii in range(1,len(d)):
        
        result2=result2^d[ii]
    result2=hex(result2)[2:len(hex(result2))].upper()
    result=hex(result)[2:len(hex(result))].upper()
    return result2,result    

def read(num):
    global com 
    if len(num)==1:
        num="000"+num
    if len(num)==2:
        num="00"+num
    if len(num)==3:
        num="0"+num        
    in0="@00RD"+str(num)+"0001"
#    print(in0)
    H,L=calCRC(in0)
    out0=in0+str(H)+str(L)+"*"+'\r'+'\n'
    print(out0)
    com.write(bytes(out0,encoding='utf-8')) 
    msgRev = com.read(30) 
    print(msgRev)
    msg=str(msgRev)
    data15=msg[7:9]
    print(msg)
    if data15!="00":
        return "error"
    data16=msg[9:13]
    print(data16)
    data10=int("0x"+data16,16)    
    return data10

def write(num,data):
    global com 
    if len(num)==1:
        num="000"+num
    if len(num)==2:
        num="00"+num
    if len(num)==3:
        num="0"+num   
        
    if len(data)==1:
        data="000"+data
    if len(data)==2:
        data="00"+data
    if len(data)==3:
        data="0"+data          
    errorCode="b'@00WD1456*\\r'"
    in0="@00WD"+str(num)+str(data)
    print(in0)
    H,L=calCRC(in0)
    print(H,L)
    out0=in0+str(H)+str(L)+"*"+'\r'+'\n'
    print(out0)
    com.write(bytes(out0,encoding='utf-8')) 
    msgRev = com.read(30) 
    print(msgRev)

#    print(msgRev)
    msg=str(msgRev)
    data16=msg[7:9]
    
    if data16!="00":
        return "error"

    print(data16)
    
    return msg
def readState():
    global com 
    a=[1<<i for i in range(0,16)]
    b=read("104")
    c=[b&ab for ab in a]
    d=[cd>0 for cd in c ]
#    print(a,b,c,d)
    return d
    
#global d100,d101,d102,d103,d104,d105,d106,d107,d108,d109,d110,com
#if __name__ == "__main__":   
#    
##    in0="@00RD10000001"
#calCRC("@00WD01000008")    
com=openSerial()
write("100","0")
readAll()
#    try:
#        a=read("100")
#        print(a)
#    except:
#        pass
#    on("101",1)
#    try:     
#        a=on("100",1)
#        print(a)
#    except:
#        pass
#    com.close()
