# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 19:15:30 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:08:18 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:09:42 2017

@author: Administrator
"""
import cv2
import numpy as np  
import threading
import time

def realcam():
    global frame,a
    a=0
    cap = cv2.VideoCapture(0)
    while(a!=2):
# get a frame  
        time.sleep(1)
        ret, frame = cap.read()        
        print(frame)
    cap.release()
    print("I am dead")
def process():
    global frame
    while(1):
        img = frame

#        cv2.imwrite("test3.jpeg", frame)
            break
global frame,a
threads = []
t1 = threading.Thread(target=realcam)
threads.append(t1)
#t2 = threading.Thread(target=process)
#threads.append(t2)
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
#    time.sleep(5)
    a=1
    while(a):
        try:   
            img=frame
            time.sleep(1)
            cv2.imshow("capture", img)
            break
        except:
            print("waiting camerer")
    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            a=2
            cv2.imwrite("test3.jpeg", frame)
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('t'):
            img=frame
            imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            try:
                circles= cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=40,minRadius=20,maxRadius=40) 
                for circle in circles[0]:
                #圆的基本信息
                    print(circle[2])
                #坐标行列
                    x=int(circle[0])
                    y=int(circle[1])
                #半径
                    r=int(circle[2])
                #在原图用指定颜色标记出圆的位置t
                    img1=cv2.circle(img,(x,y),r,(231,5,56),3)
                    cv2.putText(img1,'OK',(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(128,255,),5)
                    cv2.imshow('capture',img1)
            except:
                
                cv2.putText(img,'NG',(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
                cv2.imshow('capture',img)
                print("error")
            


#circles= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=20,minRadius=30,maxRadius=40)  
#print(circles)
#print(len(circles[0]))
##cv2.waitKey(0)  
#
#for circle in circles[0]:
#    #圆的基本信息
#    print(circle[2])
#    #坐标行列
#    x=int(circle[0])
#    y=int(circle[1])
#    #半径
#    r=int(circle[2])
#    #在原图用指定颜色标记出圆的位置
#    img=cv2.circle(img,(x,y),r,(0,0,255),3)
#cv2.imshow('res',img)
#cv2.waitKey(0)  
#cv2.destroyAllWindows()
