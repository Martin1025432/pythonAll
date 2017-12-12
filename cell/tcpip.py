# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:14:28 2017

@author: Administrator
"""
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
import time 
import win32api,win32con  
import sqlite3
import os, sys
import time

#        a=str(self.IPVar.get())
HOST = '192.168.0.30'                  #服务器IP

Port = 10001                                    #端口号
#       receivePort = 2005 
#        BUFSIZ = 1024
Addr = (HOST,Port)

Soc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字

while(1):
    try:
        Soc.connect(Addr)

        print("conn done")
        break
    except:
        time.sleep(1)
        print("waiting robot power on")
#receiveStr=str(Soc.recv(1024))  
#if receiveStr=='' :      
#    Soc.send(bytes("1",'utf8'))
    
while(1): 
       
    try:
        print("waiting data")
        receiveStr=str(Soc.recv(1024))
        print(receiveStr)
       
        if receiveStr=="b'TRG\\r'":
            print(receiveStr)
            time.sleep(1)
            Soc.send(bytes("100",'utf8'))
            break
#        if receiveStr=='2'
    except:
            print("error")
          
