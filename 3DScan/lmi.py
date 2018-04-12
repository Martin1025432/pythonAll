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
#import cv2
import System
import System.Drawing

sys.path.append(r'C:\Users\Administrator\Documents\Visual Studio 2012\Projects\lmidll\lmidll\bin\x86\Release') 

clr.FindAssembly('lmidll.dll') 
clr.FindAssembly('GoSdk.dll') 
clr.FindAssembly('GoSdkNet.dll') 
clr.FindAssembly('kkApi.dll')
clr.FindAssembly('kApiNet.dll')
clr.AddReference('kApiNet')
clr.AddReference('GoSdkNet')
clr.AddReference('lmidll')
clr.AddReference('System.Drawing')
clr.AddReference('System.IO')
clr.FindAssembly('halcondotnet.dll')
clr.AddReference('HalconDotNet')
from HalconDotNet import HObject,HOperatorSet
import System.IO
import lmidll
import Lmi3d.GoSdk;
import Lmi3d.Zen;
import Lmi3d.Zen.Io;
import Lmi3d.GoSdk.Messages as msg;
clr.AddReference('System.Runtime')
clr.AddReference('System.Runtime.InteropServices')
import System.Runtime.InteropServices
lmiObj=lmidll.sensor(())
import time
hv_AcqHandle=lmiObj.hvAcqHandle("127.0.0.1")
#----
systemObj=lmiObj.system()
sensorObj=lmiObj.sensorObj(systemObj,"127.0.0.1")
sensorObj.Connect()
setup = sensorObj.Setup
#setup.ScanMode = 3;
systemObj.EnableData(1)
#systemObj.Start()
#time.sleep(3)
#dataSet = systemObj.ReceiveData(30000000)
#dataObj=dataSet.Get(1)
#surfaceMsg=dataObj
#width = surfaceMsg.Width
#height = surfaceMsg.Length
#bufferSize = width * height
#bufferPointer = surfaceMsg.Data
#ranges=System.Array.CreateInstance(System.Int16,width*height)
##System.Runtime.InteropServices.Marshal.Copy(bufferPointer, ranges, 0, bufferSize)
#systemObj.Stop()
##ms1=System.IO.MemoryStream(ranges)
###resultBitmap = System.Drawing.Bitmap(width, height, System.Drawing.Imaging.PixelFormat.Format8bppIndexed)
##resultBitmap=System.Drawing.Bitmap(ms1)

#--------------------------
#
#ho_Image=HObject(())  
#HOperatorSet.GenEmptyObj(ho_Image)
#hv_AcqHandle=lmiObj.hvAcqHandle("192.168.1.10")  
lmiObj.grabImage(hv_AcqHandle)
#time.sleep(10)
dataSet = systemObj.ReceiveData(30000000)
ho_Image=lmiObj.getImage(hv_AcqHandle)
#HOperatorSet.CloseFramegrabber(hv_AcqHandle)
#ho_Image.Dispose()
##Do something
##convert_image_type (Image, ImageConverted, 'unit2')
#ho_GrayImage.Dispose();
lmiObj.writImage(ho_Image,"C:/Users/Administrator/pythonAll/3D x86/a3.tif")
#ho_Image.Dispose()
#--------------------------    


    
   

        
        
        























