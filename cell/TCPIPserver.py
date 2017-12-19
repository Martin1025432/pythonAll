# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 23:38:46 2017

@author: Administrator
"""
import threading
import dll
 #开始服务器进行监听  
sv = threading.Thread(target=dll.server, args=(('192.168.0.111',8000),'192.168.0.100','192.168.0.124'))
sv.start()
 #开始服务器进行监听  
 #发送指令　dll.nSoc.send(bytes('good job','utf8'))
while(1):
    try:
        if(dll.nData!=''):
            dll.nSoc.send(bytes('good job','utf8'))
            dll.nData=''
    except:
        pass





