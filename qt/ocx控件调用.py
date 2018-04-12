# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:52:44 2018

@author: Administrator
"""

#from win32com.client import Dispatch
#mp = Dispatch("MelfaRxM.ocx")
import time
import clr
import System
import System.Drawing
#import System.Windows.Forms
clr.AddReference('System.Windows.Forms')
form=System.Windows.Forms.Form()
clr.FindAssembly('Interop.MELFARXMLib.dll')  # 加载c#dll文件
clr.FindAssembly('AxInterop.MELFARXMLib.dll')  # 加载c#dll文件
clr.AddReference('Interop.MELFARXMLib')
clr.AddReference('AxInterop.MELFARXMLib')
import AxMELFARXMLib

ctrMelfaRxM=AxMELFARXMLib.AxMelfaRxM() 
((System.ComponentModel.ISupportInitialize)(ctrMelfaRxM)).BeginInit()
#a=System.Windows.Forms.Control.ControlCollection.Ctrol
form.Controls.Add(ctrMelfaRxM)
((System.ComponentModel.ISupportInitialize)(ctrMelfaRxM)).EndInit()

if ctrMelfaRxM.ServerLive()==False:
    ctrMelfaRxM.ServerStart()

def rRunMain(robot):
#修改速度
    sSendData="20"
    lStatus = ctrMelfaRxM.RequestServiceM(robot, 404, len(sSendData), sSendData, 0, 0, 0)
    time.sleep(0.5)
    sSendData="1"+"\n"+"MAINSELECT"+"\n"+"1"
    lStatus = ctrMelfaRxM.RequestServiceM(robot, 400, len(sSendData), sSendData, 0, 0, 0)  

