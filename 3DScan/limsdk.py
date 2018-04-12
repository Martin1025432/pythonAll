# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 20:46:46 2018

@author: Administrator
"""
# coding=utf-8

## clr是公共运行时环境，这个模块是与C#交互的核心
import clr
import sys
import os
import numpy as np
#import cv2
import System
import System.Drawing
import cv2
#sys.path.append(r'C:\Users\Administrator\Documents\visual studio 2012\Projects\lmidll\lmidll\bin\x86\Release') 
#clr.FindAssembly('lmidll.dll') 
#clr.FindAssembly('GoSdk.dll') 
#clr.FindAssembly('GoSdkNet.dll') 
#clr.FindAssembly('kkApi.dll')
#clr.FindAssembly('kApiNet.dll')
#clr.AddReference('kApiNet')
#clr.AddReference('GoSdkNet')
#clr.AddReference('lmidll')
#clr.AddReference('System.Drawing')
#clr.AddReference('System.IO')
clr.FindAssembly('halcondotnet.dll')
clr.AddReference('HalconDotNet')
from HalconDotNet import HObject,HOperatorSet
#import System.IO
#import lmidll
#import Lmi3d.GoSdk;
#import Lmi3d.Zen;
#import Lmi3d.Zen.Io;
#import Lmi3d.GoSdk.Messages as msg;
#clr.AddReference('System.Runtime')
#clr.AddReference('System.Runtime.InteropServices')
#import System.Runtime.InteropServices
#lmiObj=lmidll.sensor(())
#import time
#
#
#if __name__ == "__main__":
#    hv_AcqHandle=lmiObj.hvAcqHandle("192.168.1.10")
##----
#    systemObj=lmiObj.system()
#    sensorObj=lmiObj.sensorObj(systemObj,"192.168.1.10")
#    sensorObj.Connect()
#    systemObj.EnableData(1)
#    lmiObj.grabImage(hv_AcqHandle)
#    dataSet = systemObj.ReceiveData(30000000)
#    ho_Image=lmiObj.getImage(hv_AcqHandle)
#    IdValue=[]
#    for i in range(dataSet.Count):
#        dataObj=dataSet.Get(i)
#        if type(dataObj)==Lmi3d.GoSdk.Messages.GoSurfaceMsg:
#            surfaceMsg=dataObj
#            width = surfaceMsg.Width
#            height = surfaceMsg.Length
#            bufferSize = width * height
#        if type(dataObj)==Lmi3d.GoSdk.Messages.GoMeasurementMsg:
#            measurementMsg=dataObj
#            IdValue.append(measurementMsg.Get(0).Value)
#       
#        lmiObj.writImage(ho_Image,"C:/Users/Administrator/pythonAll/3D x86/a3.tif") 
#        ho_Image.Dispose()
#        HOperatorSet.CloseFramegrabber(hv_AcqHandle) 
#        img=cv2.imread("a3.tif",-1)      
#        b=img
#        g=img*100
#        r=img*200
#        mergedByNp = np.dstack([b,g,r])  
#        cv2.imwrite("aa.tif", mergedByNp) 



    
   

        
        
        























