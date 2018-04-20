# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 13:26:57 2017

@author: Administrator
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:14:28 2017

@author: Administrator
"""
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
import time 



        
def connect(HOST,Port):
    addr = (HOST,Port)    
    sock= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字   
    sock.connect(addr)
    return sock
    pass
    
def sent(sock,msg):
    sock.send(bytes(msg,'utf8'))
        
def rev(sock,size):    
    receiveStr=str(sock.recv(size)) 
    return receiveStr
    
##        a=str(self.IPVar.get())
#HOST = '192.168.100.100'                  #服务器IP
#
#Port = 2005                                    #端口号
##       receivePort = 2005 
##        BUFSIZ = 1024
#Addr = (HOST,Port)
#
#Soc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字
#
#while(1):
#    try:
#        Soc.connect(Addr)
#
#        print("conn done")
#        break
#    except:
#        time.sleep(1)
#        print("waiting robot power on")
##receiveStr=str(Soc.recv(1024))  
#receiveStr=''        
#if receiveStr=='' :      
#    Soc.send(bytes("GIM1",'utf8'))
#    
#while(1): 
#       
#    try:
#        print("waiting data")
#        receiveStr=str(Soc.recv(10240))
#        if receiveStr!='':
#            print(receiveStr)
##        if receiveStr=='2'
#    except:
#            print("error")
          

