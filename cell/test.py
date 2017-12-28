# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 00:12:05 2017

@author: Administrator
"""
import dll
import threading
import cv2
def dataProcess():
    global imgg,img,done
    while(1):
        try:

            if(str(dll.nData)=="b'TRG'"):
                cent=dll.findEdge(150,255,imgg,img,540,550,9000,20000)
                print(cent)
                dll.nSoc.send(bytes(str(cent),'utf8')) 
                dll.nData='none'
                done=1
        except:
            pass


global imgg,img,done
done=0
#cv2.namedWindow('good', cv2.WINDOW_AUTOSIZE)
sv = threading.Thread(target=dll.server, args=(('192.168.0.154',8000),'192.168.0.115','192.168.0.124'))
sv.start()
getData = threading.Thread(target=dataProcess)

img=cv2.imread('apple2.jpeg')
imgg=img.copy()
getData.start()

 #开始服务器进行监听  
 #发送指令　dll.nSoc.send(bytes('good job','utf8'))
while(1):
    if(done==1):
        done=0
        cv2.destroyAllWindows()
        cv2.namedWindow('good', cv2.WINDOW_NORMAL)    
        cv2.imshow('good',imgg)
    cv2.WaitKey(0)


        


