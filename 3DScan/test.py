# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:58:27 2018

@author: Administrator
"""
import socketClient 
import time
sock=socketClient.connect("127.0.0.1",23)
socketClient.sent(sock,"jjjk")
msg=socketClient.rev(sock,1024)
print(msg)
#while(1): 
#       
#    try:
#        print("waiting data")
#        receiveStr=socketClient.rev(sock,1024)



