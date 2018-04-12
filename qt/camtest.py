# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:12:44 2018

@author: Administrator
"""

import clr
import cv2
import System
import System.Drawing
import time
clr.FindAssembly('PylonC.NET.dll')  # 加载c#dll文件
clr.FindAssembly('PylonC.NETSupportLibrary.dll')  # 加载c#dll文件
clr.FindAssembly('Basler.Pylon.dll')  # 加载c#dll文件
clr.AddReference('PylonC.NET')
clr.AddReference('Basler.Pylon')
clr.AddReference('PylonC.NETSupportLibrary')
from PylonC.NET import *
from PylonC.NETSupportLibrary import *
from Basler.Pylon import *

camDic=[105,105,105,105]
def CapIni(sn):
    try:
        camera = [Camera(sn[i]) for i in range(len(sn))]
    except Exception as e:
        print(str(e))
    for i in range(len(camera)):
        camera[i].CameraOpened += Configuration.AcquireSingleFrame
        #camera.CameraOpened += Configuration.AcquireSingleFrame
        #AcquireContinuous
        camera[i].Open()


        b=camera.Parameters[PLCamera.ExposureTimeRaw].SetValue(35)

        print(a,c)

camera.StreamGrabber.Start()
grabResult = camera.StreamGrabber.RetrieveResult(5000, TimeoutHandling.ThrowException)
ImagePersistence.Save(ImageFileFormat.Bmp, "test.bmp", grabResult)
camera.StreamGrabber.Stop()
camera.Close()
#a=camera.StreamGrabber.Start(1, GrabStrategy.OneByOne, GrabLoop.ProvidedByStreamGrabber)
#while camera.StreamGrabber.IsGrabbing:
#    print("wait")