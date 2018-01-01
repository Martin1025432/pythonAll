# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 18:54:22 2017

@author: Administrator
"""

from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
import time 
HOST = '192.168.100.3'                          #服务器IP
sentPort = 2006                                     #端口号
receivePort = 2005 
BUFSIZ = 1024
sentAddr = (HOST,sentPort)
receiveAddr = (HOST,receivePort)

sentSoc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字
receiveSoc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字
sentSoc.connect(sentAddr)                        #尝试连接服务器
receiveSoc.connect(receiveAddr)  
receiveSoc.setblocking(False)

while True:
    a=input("waiting for order:")  
    
    if a=="t" :
        try:
            b=str(receiveSoc.recv(1024))
        except:
            print("error")
        sentSoc.send(bytes("TRG",'utf8'))  

    if a=="c" :

        sentSoc.send(bytes("CJB002",'utf8'))  
        time.sleep(2)              
        sentSoc.send(bytes("TRG",'utf8'))      
    if a=="cc" :

        sentSoc.send(bytes("CJB003",'utf8'))  
        time.sleep(2)              
        sentSoc.send(bytes("TRG",'utf8'))  
        
    if a=="p" :

        sentSoc.send(bytes("CJB003",'utf8')) 
        
    if a=="n":

        sentSoc.send(bytes("CJB002",'utf8')) 
    if a=="g":
        try:
            b=str(receiveSoc.recv(1024))
            c=int(b[2:-2])
        except:
            b=""
        print(b)
    if a=="a":
        valueF=0
        valueB=20
        while((valueB-valueF)>=5):
            valueFstr=""
            try:
                valueFstr=str(receiveSoc.recv(1024))
            except:
                    print("error")
            sentSoc.send(bytes("CJB001",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            time.sleep(1)
            while valueFstr=="" :
                try:
                    valueFstr=str(receiveSoc.recv(1024))
                
                except:
                    print("error")
                
            valueF=int(valueFstr[2:-1])
            print(valueF,"pf")
            sentSoc.send(bytes("CJB002",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            valueBstr=""
            time.sleep(1)
            sentSoc.send(bytes("CJB001",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            time.sleep(1)
            valueBstr="" 
            valueB=0
            try:
                valueBstr=str(receiveSoc.recv(1024))
                print(valueBstr,"pb")
            except:
                print("error")
            valueB=int(valueBstr[2:-1])  
            print(valueB)
        valueF=0
        valueB=20 
           
        while((valueB-valueF)>=5):
            valueFstr=""
            try:
                valueFstr=str(receiveSoc.recv(1024))
            except:
                    print("error")
            sentSoc.send(bytes("CJB001",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            time.sleep(1)
            while valueFstr=="" :
                try:
                    valueFstr=str(receiveSoc.recv(1024))
                
                except:
                    print("error")
                
            valueF=int(valueFstr[2:-1])
            print(valueF,"nf")
            sentSoc.send(bytes("CJB003",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            valueBstr=""
            time.sleep(1)
            sentSoc.send(bytes("CJB001",'utf8')) 
            time.sleep(1)
            sentSoc.send(bytes("TRG",'utf8')) 
            time.sleep(1)
            valueBstr="" 
            valueB=0
            try:
                valueBstr=str(receiveSoc.recv(1024))
                print(valueBstr,"nb")
            except:
                print("error")
            valueB=int(valueBstr[2:-1])  
            print(valueB)        

            
        
       
            
        
        
        
        
                
                
            
        
 
        

