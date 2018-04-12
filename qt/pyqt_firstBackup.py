from __future__ import division
import clr
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage,QStandardItem
from PyQt5.QtCore import QThread ,  pyqtSignal
from PyQt5.QtWidgets import QFileDialog ,QTableWidgetItem
import time
import inspect 
import sqlite3
import pandas
import collections  
import cv2
import math
#import dll
from ctypes import * 
import visionpro
import threading
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
#import cv2
import numpy as np
import win32api,win32con  
import os, sys
import System
import System.Drawing
#import time
#from PyQt5 import *
#import datetime
import time
import win32com.client
import xml.etree.ElementTree as ET
  
#三菱ROBOT控制件－－－－－－－－－－－－
clr.AddReference('System.Windows.Forms')
form=System.Windows.Forms.Form()
clr.FindAssembly('Interop.MELFARXMLib.dll')  # 加载c#dll文件
clr.FindAssembly('AxInterop.MELFARXMLib.dll')  # 加载c#dll文件
clr.AddReference('Interop.MELFARXMLib')
clr.AddReference('AxInterop.MELFARXMLib')
import AxMELFARXMLib


#三菱ROBOT控制件－－－－－－－－－－－－－－－

#BASLER－－－－－－－－－－－－－－－
clr.FindAssembly('PylonC.NET.dll')  # 加载c#dll文件
clr.FindAssembly('PylonC.NETSupportLibrary.dll')  # 加载c#dll文件
clr.FindAssembly('Basler.Pylon.dll')  # 加载c#dll文件
clr.AddReference('PylonC.NET')
clr.AddReference('Basler.Pylon')
clr.AddReference('PylonC.NETSupportLibrary')
from PylonC.NET import *
from PylonC.NETSupportLibrary import *
from Basler.Pylon import *
#BASLER－－－－－－－－－－－－－－－
qtCreatorFile = "window.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类

#---初始化
    def __init__(self):
        global  cursor, p ,conn ,dictPara,basler,sn ,fd  ,camFlag ,mod, serverFlag, expos,exposCalc                 #初始化
        global pSheetRealTimeFlag,pPlateRealTimeFlag,nSheetRealTimeFlag,nPlateRealTimeFlag,trigCalc,trigCalcFlag,trigCalcFlag1,trigCalcFlag2,trigCalcFlag3
        global countPsheetCalc,MposiontCodDic,pSheetToolFlag,pSheetToolNextFlag,bPplateToolNextFlag,bPplateToolFlag, nSheetToolFlag, nSheetToolNextFlag
        global ctrMelfaRxM,snDic,countNsheetCalc, bNplateToolFlag,bNplateToolNextFlag
        global r1SVflage,r2SVflage,tablePs,autoFlag,tableNs,calcFlag,R1Do1_ON,R1Do2_ON,R2Do1_ON,R2Do2_ON
        global countPsheetOK,countPsheetNG,countNsheetOK,countNsheetNG,countPplateOK,countPplateNG,countNplateOK,countNplateNG
        global countPsheetFail,countNsheetFail,countPplateFail,countNplateFail
        global pix21,pix22,pix11,pix12
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        #---加载sqlite3参数数据库，程序所有参数
        conn = sqlite3.connect("cm08.db")
        cursor = conn.cursor()
        self.sqlUpdate()
        #---加载ACCESS产量数据库
#        conn = win32com.client.Dispatch(r'ADODB.Connection')
#        DSN = 'PROVIDER=Microsoft.ACE.OLEDB.12.0;DATA SOURCE=C:/test.mdb;'
#        conn.Open(DSN)
#        #打开表
#        rs = win32com.client.Dispatch(r'ADODB.Recordset')
#        rs_name = 'sheet'#表名
#        rs.Open('[' + rs_name + ']', conn, 1, 3)        
        #---主界面按钮
        #数据复位，保存      
        self.bDataReset.clicked.connect(self.bDataResetClick)
        self.bDataSave.clicked.connect(self.bDataSaveClick)     
        self.bAuto.clicked.connect(self.bAutoClick) 
        #机器人操作面板
        self.bR1run.clicked.connect(self.bR1runClick)
        self.bR1stop.clicked.connect(self.bR1stopClick) 
        self.bR1reset.clicked.connect(self.bR1resetClick)        
        self.bR1server.clicked.connect(self.bR1serverClick)         
        self.bR2run.clicked.connect(self.bR2runClick)
        self.bR2stop.clicked.connect(self.bR2stopClick) 
        self.bR2reset.clicked.connect(self.bR2resetClick)        
        self.bR2server.clicked.connect(self.bR2serverClick)   
        self.bRreconnect.clicked.connect(self.bRreconnectClick)
        self.bRconnectOff.clicked.connect(self.bRconnectOffClick)
                        
        #开启网络，连接相机       
        self.bTCPini_2.clicked.connect(self.bTCPiniClick)
        self.bCamIni.clicked.connect(self.bCamIniClick)
                        
        #---检测设定界面按钮
        #浏览
        self.bSelectDoc.clicked.connect(self.bSelectDocClick)
        
        #---视觉调试界面按钮
        
        
        
        
        #视觉触发选择       
        self.radioCalc.toggled.connect(self.radioCalcClick)          
                             
        #位置组合标定       
        self.bPpostionCalc.clicked.connect(self.bPpostionCalclick)          
        self.bNpostionCalc.clicked.connect(self.bNpostionCalclick)         
        
        
        #更新曝光时间       
        self.bUpdateCam.clicked.connect(self.bUpdateCamClick)        
        #实时，触发
        self.bPsheetTrig.clicked.connect(self.bPsheetTrigClick)  
        self.bPplateTrig.clicked.connect(self.bPplateTrigClick) 
        self.bNsheetTrig.clicked.connect(self.bNsheetTrigClick) 
        self.bNplateTrig.clicked.connect(self.bNplateTrigClick)
        self.bUpdateCam.clicked.connect(self.bUpdateCamClick)
        self.bRealTimePsheet.clicked.connect(self.bRealTimePsheetClick)
        self.bRealTimePplate.clicked.connect(self.bRealTimePplateClick)
        self.bRealTimeNsheet.clicked.connect(self.bRealTimeNsheetClick)
        self.bRealTimeNplate.clicked.connect(self.bRealTimeNplateClick)               
        #标定
        #   9点位置示孝---------- 
        self.bR1SetPT31.clicked.connect(self.bR1SetPT31Click)
        self.bR1SetPT32.clicked.connect(self.bR1SetPT32Click)
        self.bR1SetPT33.clicked.connect(self.bR1SetPT33Click)
        self.bR1SetPT21.clicked.connect(self.bR1SetPT21Click)
        self.bR1SetPT22.clicked.connect(self.bR1SetPT22Click)
        self.bR1SetPT23.clicked.connect(self.bR1SetPT23Click)        
        
        self.bR2SetPT31.clicked.connect(self.bR2SetPT31Click)
        self.bR2SetPT32.clicked.connect(self.bR2SetPT32Click)
        self.bR2SetPT33.clicked.connect(self.bR2SetPT33Click)
        self.bR2SetPT21.clicked.connect(self.bR2SetPT21Click)
        self.bR2SetPT22.clicked.connect(self.bR2SetPT22Click)
        self.bR2SetPT23.clicked.connect(self.bR2SetPT23Click)        
        #   正极过渡片----------    

        self.bPsheetCalc.clicked.connect(self.bPsheetCalcClick) 
        self.bPsheetUpdateTable.clicked.connect(self.bPsheetUpdateTableClick)
        self.bPsheetToolCalc.clicked.connect(self.bPsheetToolCalcClick)
        self.bPsheetToolCalcNext.clicked.connect(self.bPsheetToolCalcNextClick)    
        self.bR1SetPT31
        
        #   正极盖板-------------

        self.bPplateCalc.clicked.connect(self.bPplateCalcClick) 
        self.bPplateUpdateTable.clicked.connect(self.bPplateUpdateTableClick)  
        self.bPplateToolCalc.clicked.connect(self.bPplateToolCalcClick)
        self.bPplateToolCalcNext.clicked.connect(self.bPplateToolCalcNextClick)              
        #   负极过渡片------------

        self.bNsheetCalc.clicked.connect(self.bNsheetCalcClick) 
        self.bNsheetUpdateTable.clicked.connect(self.bNsheetUpdateTableClick) 
        self.bNsheetToolCalc.clicked.connect(self.bNsheetToolCalcClick)
        self.bNsheetToolCalcNext.clicked.connect(self.bNsheetToolCalcNextClick)

             
        #   负极盖板------------

        self.bNplateCalc.clicked.connect(self.bNplateCalcClick)
        self.bNplateUpdateTable.clicked.connect(self.bNplateUpdateTableClick) 
        self.bNplateToolCalc.clicked.connect(self.bNplateToolCalcClick)
        self.bNplateToolCalcNext.clicked.connect(self.bNplateToolCalcNextClick)                
               
        #---机器人手动界面按钮
        #机器人操作面板1---        
        self.bR1Mgo1.clicked.connect(self.bR1Mgo1Click)
        self.bR1Mgo2.clicked.connect(self.bR1Mgo2Click)
        self.bR1Mgo3.clicked.connect(self.bR1Mgo3Click)
        self.bR1Mgo4.clicked.connect(self.bR1Mgo4Click)
        self.bR1Mgo5.clicked.connect(self.bR1Mgo5Click)
        self.bR1Mgo6.clicked.connect(self.bR1Mgo6Click)
        self.bR1Mgo7.clicked.connect(self.bR1Mgo7Click) 
        self.bR1Mio1.clicked.connect(self.bR1Mio1Click) 
        self.bR1Mio2.clicked.connect(self.bR1Mio2Click) 

        
        self.bR1Mgo1Set.clicked.connect(self.bR1Mgo1SetClick)
        self.bR1Mgo2Set.clicked.connect(self.bR1Mgo2SetClick)
        self.bR1Mgo3Set.clicked.connect(self.bR1Mgo3SetClick)
        self.bR1Mgo4Set.clicked.connect(self.bR1Mgo4SetClick)
        self.bR1Mgo5Set.clicked.connect(self.bR1Mgo5SetClick)
        self.bR1Mgo6Set.clicked.connect(self.bR1Mgo6SetClick)
        self.bR1Mgo7Set.clicked.connect(self.bR1Mgo7SetClick)        
        
        self.bR1YPgo.clicked.connect(self.bR1YPgoClick)
        self.bR1YNgo.clicked.connect(self.bR1YNgoClick)
        self.bR1XPgo.clicked.connect(self.bR1XPgoClick)
        self.bR1XNgo.clicked.connect(self.bR1XNgoClick)   
        self.bR1ZPgo.clicked.connect(self.bR1ZPgoClick)
        self.bR1ZNgo.clicked.connect(self.bR1ZNgoClick)         
        self.bR1CPgo.clicked.connect(self.bR1CPgoClick)
        self.bR1CNgo.clicked.connect(self.bR1CNgoClick)
        

        #机器人操作面板2---        
        self.bR2Mgo1.clicked.connect(self.bR2Mgo1Click)
        self.bR2Mgo2.clicked.connect(self.bR2Mgo2Click)
        self.bR2Mgo3.clicked.connect(self.bR2Mgo3Click)
        self.bR2Mgo4.clicked.connect(self.bR2Mgo4Click)
        self.bR2Mgo5.clicked.connect(self.bR2Mgo5Click)
        self.bR2Mgo6.clicked.connect(self.bR2Mgo6Click)
        self.bR2Mgo7.clicked.connect(self.bR2Mgo7Click)     
        self.bR2Mio1.clicked.connect(self.bR2Mio1Click) 
        self.bR2Mio2.clicked.connect(self.bR2Mio2Click)
        
        self.bR2Mgo1Set.clicked.connect(self.bR2Mgo1SetClick)
        self.bR2Mgo2Set.clicked.connect(self.bR2Mgo2SetClick)
        self.bR2Mgo3Set.clicked.connect(self.bR2Mgo3SetClick)
        self.bR2Mgo4Set.clicked.connect(self.bR2Mgo4SetClick)
        self.bR2Mgo5Set.clicked.connect(self.bR2Mgo5SetClick)
        self.bR2Mgo6Set.clicked.connect(self.bR2Mgo6SetClick)
        self.bR2Mgo7Set.clicked.connect(self.bR2Mgo7SetClick)           
                
        self.bR2YPgo.clicked.connect(self.bR2YPgoClick)
        self.bR2YNgo.clicked.connect(self.bR2YNgoClick)
        self.bR2XPgo.clicked.connect(self.bR2XPgoClick)
        self.bR2XNgo.clicked.connect(self.bR2XNgoClick)   
        self.bR2ZPgo.clicked.connect(self.bR2ZPgoClick)
        self.bR2ZNgo.clicked.connect(self.bR2ZNgoClick)         
        self.bR2CPgo.clicked.connect(self.bR2CPgoClick)
        self.bR2CNgo.clicked.connect(self.bR2CNgoClick)
        
        self.bR1save.clicked.connect(self.bR1saveClick)
        self.bR2save.clicked.connect(self.bR2saveClick)
        
        
        #---QT界面数据刷新线程                
        self.thread = MyThread()
        self.thread.setIdentity("thread1")
        self.thread.sinOut.connect(self.GUIfresh)
        self.thread.setVal(2)        
                
#        fd = os.open( "debug.txt", os.O_RDWR|os.O_APPEND )                   
        #---QT界面初始化        
        #标定控件隐藏效果
        self.bPsheetToolCalcNext.hide()
        self.bPplateToolCalcNext.hide()
        self.bNsheetToolCalcNext.hide()
        self.bNplateToolCalcNext.hide()
        self.tR1Mspeed.setText("10")
        self.tR2Mspeed.setText("10")
        #视学调试，表格标题
        self.tableWidgetPs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
        self.tableWidgetPp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
        self.tableWidgetNs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y'])  
        self.tableWidgetNp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
        #产量数据
        self.tPsheetTotal.setText(dictPara['tPsheetTotal'])
        self.tPsheetGood.setText(dictPara['tPsheetGood'])
        self.tPsheetGoodRate.setText(dictPara['tPsheetGoodRate'])
        self.tPsheetBad.setText(dictPara['tPsheetBad'])
        self.tPsheetBadRate.setText(dictPara['tPsheetBadRate'])
        self.tPsheetFail.setText(dictPara['tPsheetFail'])
        self.tPplateTotal.setText(dictPara['tPplateTotal'])
        self.tPplateGood.setText(dictPara['tPplateGood'])
        self.tPplateGoodRate.setText(dictPara['tPplateGoodRate'])
        self.tPplateBad.setText(dictPara['tPplateBad'])
        self.tPplateBadRate.setText(dictPara['tPplateBadRate'])
        self.tPplateFail.setText(dictPara['tPplateFail'])
        self.tNsheetTotal.setText(dictPara['tNsheetTotal'])
        self.tNsheetGood.setText(dictPara['tNsheetGood'])
        self.tNsheetGoodRate.setText(dictPara['tNsheetGoodRate'])
        self.tNsheetBad.setText(dictPara['tNsheetBad'])
        self.tNsheetBadRate.setText(dictPara['tNsheetBadRate'])
        self.tNsheetFail.setText(dictPara['tNsheetFail'])
        self.tNplateTotal.setText(dictPara['tNplateTotal'])
        self.tNplateGood.setText(dictPara['tNplateGood'])
        self.tNplateGoodRate.setText(dictPara['tNplateGoodRate'])
        self.tNplateBad.setText(dictPara['tNplateBad'])
        self.tNplateBadRate.setText(dictPara['tNplateBadRate'])
        self.tNplateFail.setText(dictPara['tNplateFail'])
        self.tTime.setText(dictPara['tTime'])
        self.tPsheetSn.setText(dictPara['tPsheetSn'])
        self.tNsheetSn.setText(dictPara['tNsheetSn'])
        self.tPplateSn.setText(dictPara['tPplateSn'])
        self.tNplateSn.setText(dictPara['tNplateSn'])
        #机器人IP参数       
        self.tPip.setText(dictPara['tPip'])
        self.tNip.setText(dictPara['tNip'])
        self.tTCPport.setText(dictPara['tTCPport'])
        self.tIP.setText(dictPara['tIP'])        
        #视觉判定参数
        #   正极过渡片
        self.tPsheetStandX.setText(dictPara['tPsheetStandX'])
        self.tPsheetStandY.setText(dictPara['tPsheetStandY'])
        self.tPsheetBadValue.setText(dictPara['tPsheetBadValue'])
        self.tPsheetBadDegreeValue.setText(dictPara['tPsheetBadDegreeValue'])
        
        self.tPsheetStandR.setText(dictPara['tPsheetStandR'])
        self.tPsheetOffsetR.setText(dictPara['tPsheetOffsetR'])
        self.tPsheetStandD.setText(dictPara['tPsheetStandD'])
        self.tPsheetPixMM.setText(dictPara['tPsheetPixMM'])

        #   正极盖板
        self.tPplateStandX.setText(dictPara['tPplateStandX'])
        self.tPplateStandY.setText(dictPara['tPplateStandY'])
        self.tPplateBadValue.setText(dictPara['tPplateBadValue'])
        self.tPplateBadDegreeValue.setText(dictPara['tPplateBadDegreeValue'])
        self.tPplatePixMM.setText(dictPara['tPplatePixMM'])
        
        self.tPplateStandR.setText(dictPara['tPplateStandR'])
        self.tPplateOffsetR.setText(dictPara['tPplateOffsetR'])
        self.tPplateStandD.setText(dictPara['tPplateStandD'])
        #   负极过渡片
        self.tNsheetStandX.setText(dictPara['tNsheetStandX'])
        self.tNsheetStandY.setText(dictPara['tNsheetStandY'])
        self.tNsheetBadValue.setText(dictPara['tNsheetBadValue'])
        self.tNsheetBadDegreeValue.setText(dictPara['tNsheetBadDegreeValue'])
        self.tNsheetStandR.setText(dictPara['tNsheetStandR'])
        self.tNsheetOffsetR.setText(dictPara['tNsheetOffsetR'])
        self.tNsheetStandD.setText(dictPara['tNsheetStandD'])    
        self.tNsheetPixMM.setText(dictPara['tNsheetPixMM'])
        #   负极盖板
        self.tNplateStandX.setText(dictPara['tNplateStandX'])
        self.tNplateStandY.setText(dictPara['tNplateStandY'])
        self.tNplateBadValue.setText(dictPara['tNplateBadValue'])    
        self.tNplateBadDegreeValue.setText(dictPara['tNplateBadDegreeValue'])        
        self.tNplateStandR.setText(dictPara['tNplateStandR'])
        self.tNplateOffsetR.setText(dictPara['tNplateOffsetR'])
        self.tNplateStandD.setText(dictPara['tNplateStandD'])  
        self.tNplatePixMM.setText(dictPara['tNplatePixMM'])
        #不良品路径
        self.tNGpath.setText(dictPara['tNGpath']) 
        #曝光时间
        self.tExposureTimeRawPsheet.setText(dictPara['tExposureTimeRawPsheet'])
        self.tExposureTimeRawPplate.setText(dictPara['tExposureTimeRawPplate'])
        self.tExposureTimeRawNsheet.setText(dictPara['tExposureTimeRawNsheet'])
        self.tExposureTimeRawNplate.setText(dictPara['tExposureTimeRawNplate'])             
        
        #---全局变量初始化
        tablePs=[["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"]]
        tableNs=[["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0"]]
        R1Do1_ON=0
        R1Do2_ON=0
        R2Do1_ON=0
        R2Do2_ON=0        
        pCalcFlag=0
        nCalcFlag=0
        calcFlag=0
        mod=0
        camFlag=0
        serverFlag=0
        pSheetRealTimeFlag=0
        trigCalc=0
        
        trigCalcFlag=0
        trigCalcFlag1=0
        trigCalcFlag2=0
        trigCalcFlag3=0
        
        pPlateRealTimeFlag=0
        nPlateRealTimeFlag=0        
        nSheetRealTimeFlag=0
        nSheetToolFlag=0
        nSheetToolNextFlag=0
        bNplateToolNextFlag=0
        bNplateToolFlag=0        
        pSheetToolFlag=0
        pSheetToolNextFlag=0        
        bPplateToolNextFlag=0        
        bPplateToolFlag=0
        
        r1SVflage=0
        r2SVflage=0  
        
        countPsheetCalc=0
        countNsheetCalc=0



        countPsheetOK=int(dictPara['tPsheetGood'])
        countPsheetNG=int(dictPara['tPsheetBad'])
        countNsheetOK=int(dictPara['tNsheetGood'])
        countNsheetNG=int(dictPara['tNsheetBad'])
        countPplateOK=int(dictPara['tPplateGood'])
        countPplateNG=int(dictPara['tPplateBad'])
        countNplateOK=int(dictPara['tNplateGood'])
        countNplateNG=int(dictPara['tNplateBad'])
        
        countPsheetFail=int(dictPara['tPsheetFail'])
        countNsheetFail=int(dictPara['tNsheetFail'])        
        countPplateFail=int(dictPara['tPplateFail'])
        countNplateFail=int(dictPara['tNplateFail'])
        pix21=int(dictPara['tNsheetPixMM'])
        pix22=int(dictPara['tNplatePixMM'])
        pix11=int(dictPara['tPsheetPixMM'])
        pix12=int(dictPara['tPplatePixMM'])        
        autoFlag=0
        MposiontCodDic={ self.tMp1.placeholderText(): self.tMcode1.placeholderText(),self.tMp2.placeholderText(): self.tMcode2.placeholderText(),self.tMp3.placeholderText(): self.tMcode3.placeholderText(),
                        self.tMp4.placeholderText(): self.tMcode4.placeholderText(),self.tMp5.placeholderText(): self.tMcode5.placeholderText(),self.tMp6.placeholderText(): self.tMcode6.placeholderText(), 
                        self.tMp7.placeholderText(): self.tMcode7.placeholderText()}
#        snDic={0:"bmpForProcess0.bmp",1:"bmpForProcess1.bmp",2:"bmpForProcess2.bmp",3:"bmpForProcess3.bmp"}
        #---启动子程序
        visionpro.visionproLoad()
        self.rOCXrun()                        
        self.bCamIniClick()
        self.bTCPiniClick()    


#---事件     
    def closeEvent(self, event):
        global ctrMelfaRxM
        try:
            self.rStop(1)
            self.rReset(1)
            self.rStop(2)
            self.rReset(2)
            ctrMelfaRxM.ServerKill()
        except:
            pass
        self.close()
        os._exit(0)
        
#---主界面按钮事件 
    #---连接相机
    def bCamIniClick(self):
        global  cursor, p ,conn ,dictPara,basler,sn ,fd , camFlag,mod    
        if camFlag==0:
           # print("camFlag:",camFlag)
            try:
                self.camIni()
#                for i in range(0,4):  
#                    sizebuffer=basler.outputStr(i)
#                    print(c_char_p(sizebuffer).value)
#                    recStr=str(c_char_p(sizebuffer).value)[2:-1]
#                    sn.append(recStr)
                self.bCamIni.setStyleSheet("background-color: rgb(0, 255, 0);")
                camFlag=1
                mod=1
                print("camFlag,mod:",camFlag,mod)

            except Exception as e:
                self.outDebug("相机打开失败")
                b=win32api.MessageBox(0, "相机打开失败，请手动开启", "相机初始化",win32con.MB_OK)        
                self.bCamIni.setStyleSheet("background-color: rgb(255, 0, 0);")
                camFlag=0
                mod=0

                print(str(e))
        
        else:
            self.capEnd()
            self.bCamIni.setStyleSheet("background-color: rgb(255, 0, 0);")
            camFlag=0
            mod=0
           # print("camFlag:",camFlag)
            
    #---TCPIP        
    def bTCPiniClick(self):
        global serverFlag,sv,serverSoc,tp,tn,pSoc,nSoc
    
        addr=(dictPara['tIP'],int(dictPara['tTCPport']))
        print(addr)
        if serverFlag==0:  
            sv = threading.Thread(target=self.server, args=(addr,dictPara['tNip'],dictPara['tPip']))
#            sv.setDaemon(True) #设
            print(sv,serverFlag)
            sv.start()
            print(sv,serverFlag)
            serverFlag=1
            return 0
        if serverFlag==1:
            try:
                serverFlag=0
                serverSoc.close()
            except Exception as e:
                print(str(e))
                
            try:    
                self.stop_thread(sv)
            except Exception as e:
                print(str(e))
            
            try:    
                pSoc.close()
                self.stop_thread(tp)
            except Exception as e:  
                print(str(e))
                
            try:    
                nSoc.close()
                self.stop_thread(tn)
            except Exception as e:                 
                print(str(e))
                

            self.bTCPini_2.setStyleSheet("background-color: rgb(255, 0, 0);")
            print(sv,serverFlag)
            return 0
    def server(self,serverAddr,nClientIP,pClientIP):
        global nData,pData,nSoc,pSoc ,serverFlag,serverSoc,tn,tp
        mulLock = threading.Lock()  
        try:
            serverSoc = socket(AF_INET, SOCK_STREAM)
            serverSoc.bind(serverAddr)
            serverSoc.listen(2)
            self.outDebug("开启服务器成功")
            self.bTCPini_2.setStyleSheet("background-color: rgb(0, 255, 0);")
            serverFlag=1
        except Exception as e:
            self.outDebug("开启服务器失败"+str(e))
            b=win32api.MessageBox(0, "开启服务器失败，请检查IP地址和网络连", "开启服务器",win32con.MB_OK) 
            self.bTCPini_2.setStyleSheet("background-color: rgb(255, 0, 0);")
            serverFlag=0
            return -1

            
        while True:
    # 接受一个新连接:
            sock, addr = serverSoc.accept()
            if(addr[0]==nClientIP):
    # 创建新线程来处理TCP连接:
                print(sock)
                self.outDebug("负极客端连接成功:"+str(sock))
                nData='conned'
                              
                nSoc=sock 
                tn = threading.Thread(target=self.tcplink, args=(sock, addr,nClientIP,pClientIP))
                tn.start()
                print('nclien',nData)
                
                
            if(addr[0]==pClientIP):
    # 创建新线程来处理TCP连接:
                print(addr)
                self.outDebug("正极客端连接成功:"+str(sock))
                pData='conned'
                
                pSoc=sock   
                pSoc.setblocking(0)
                sock.setblocking(0)
                try:                
                    tp = threading.Thread(target=self.tcplink, args=(sock, addr,nClientIP,pClientIP))
                    tp.start()
                    print('pclien',pData)
                except:
                    print('error')
                    
    def tcplink(self,sock, addr,nClientIP,pClientIP):
        global nData,pData,nSoc,pSoc,centPsheet, centNsheet,centPplate, centNplate,countPsheetCalc,countNsheetCalc,pCalcFlag,nCalcFlag,tablePs,tablePp,tableNs,tableNp
        global calcFlag,pix11,pix12,pix21,pix22
        while True:
            try:
                data = sock.recv(1024)
                #print("data:")
                if(data!=''):
                    if(addr[0]==nClientIP):
                        nData=data
                        print("nData:",nData)
                        self.outDebug("收收负极机器人信息:"+str(nData))
                        #self.tNrec.setText(str(nData))
                        if(nData==b'TRGS\r'):

                            time.sleep(0.5)
                            centN,lineN,resultN=self.bNsheetTrigClick()
                            print("centN:",str(centN[0]),str(centN[1]))
                            print(str(centN[0])+","+str(centN[1]))
                            outCent=str(centN[0])+","+str(centN[1])
                            print("centN:",outCent,lineN) 
                            if calcFlag==0:
                                outCent=outCent+","+str(lineN)
                                
                                print("centN:",outCent) 
                            try:
                                nSoc.send(bytes(outCent,'utf8'))
                                pass
                            except:
                                print("erro find")    
                            nData=b''
                        if(nData==b'TRGP\r'):
                            
                            time.sleep(0.5)
                            centN,lineN,resultN=self.bNplateTrigClick()

                            outCent=str(centN[0])+","+str(centN[1])
                            
                            print("centN:",outCent,lineN) 
                            if calcFlag==0:
                                outCent=outCent+","+str(lineN)
                                
                                print("centN:",outCent) 
                            print("TRGP,OUTDATA:",outCent)
                            try:
                                nSoc.send(bytes(outCent,'utf8'))
                                pass
                            except:
                                print("erro find")    
                            nData=b''   
                        if(str(nData)[2:4]=="XY"):
                            countNsheetCalc=countNsheetCalc+1
                            inputData=str(nData)[16:len(str(nData))]                            
                            inputX=float(inputData[0:10])
                            inputY=float(inputData[14:-3])    
                            print(inputX,inputY)
                            print("count",countNsheetCalc)
                            if countNsheetCalc<10:
                                nSoc.send(bytes("1",'utf8'))
                                tableNs[2][countNsheetCalc-1]=str(centN[0])
                                tableNs[3][countNsheetCalc-1]=str(centN[1])
                                tableNs[0][countNsheetCalc-1]=str(inputX)
                                tableNs[1][countNsheetCalc-1]=str(inputY)                                                                  
                                print("tableNs:",tableNs)

                            else:
                                
                              
                                nSoc.send(bytes("90",'utf8'))

                                countNsheetCalc=0
                            nData=b'' 
                            
                        if(str(nData)[2:5]=="PIX"):
                            print("nData")
                            inputData=str(nData)[16:len(str(nData))]                            
                            dx1=float(inputData[0:10])
                            dy1=float(inputData[14:24])
                            dx2=float(inputData[28:38])
                            dy2=float(inputData[42:52])
                                                    
                            print("dx1,dy1,dx2,dy2",dx1,dy1,dx2,dy2)
                            pix21=round(sqrt(dx1**2+dy1**2),3)
                            pix22=round(sqrt(dx2**2+dy2**2),3)
                            nData=b'' 

                                                                                                                          
                    if(addr[0]==pClientIP):
                        pData=data 
                        print("pData:",pData)
                        self.outDebug("收到正极机器人信息:"+str(pData))
                        #self.tPrec.setText(str(pData))
                        if(pData==b'TRGSA\r'):

                            time.sleep(0.2)
                            centP,lineP,resultP=self.bPsheetTrigClick()
                            
                            print("centP:",str(centP[0]),str(centP[1]))
                            print(str(centP[0])+","+str(centP[1]))
                            outCent=str(centP[0])+","+str(centP[1])
                            if calcFlag==0:
                                outCent=str(centN[0])+","+str(centN[1])+","+str(lineN)
                            try:
                                pSoc.send(bytes(outCent,'utf8'))
                                pass
                            except:
                                print("erro find")    
                            nData=b''                        
                        
                        
                        
                        if(pData==b'TRGS\r'):

                            time.sleep(0.2)
                            centP,lineP,resultP=self.bPsheetTrigClick()
                            
                            print("centP:",str(centP[0]),str(centP[1]))
                            print(str(centP[0])+","+str(centP[1]))
                            outCent=str(centP[0])+","+str(centP[1])
                            if calcFlag==0:
                                outCent=str(centN[0])+","+str(centN[1])+","+str(lineN)
                            try:
                                pSoc.send(bytes(outCent,'utf8'))
                                pass
                            except:
                                print("erro find")    
                            pData=b''
                            
                        if(pData==b'TRGP\r'):

                            centP,lineP,resultP=self.bPplateTrigClick()
                            print("centP:",str(centP[0]),str(centP[1]))
                            print(str(centP[0])+","+str(centP[1]))
                            outCent=str(centP[0])+","+str(centP[1])
                            if calcFlag==0:
                                outCent=str(centN[0])+","+str(centN[1])+","+str(lineN)                            
                            try:
                                pSoc.send(bytes(outCent,'utf8'))
                                pass
                            except:
                                print("erro find")    
                            pData=b''  
                            
                        if(str(pData)[2:4]=="XY"):
                            countPsheetCalc=countPsheetCalc+1
                            inputData=str(pData)[16:len(str(pData))]                            
                            inputX=float(inputData[0:10])
                            inputY=float(inputData[14:-3])    
                            print(inputX,inputY)
                            print("count",countPsheetCalc)
                            if countPsheetCalc<10:
                                tablePs[2][countPsheetCalc-1]=str(centP[0])
                                tablePs[3][countPsheetCalc-1]=str(centP[1])
                                tablePs[0][countPsheetCalc-1]=str(inputX)
                                tablePs[1][countPsheetCalc-1]=str(inputY)                                  
                                pSoc.send(bytes("1",'utf8'))

                                print("tablePs:",tablePs)

                            else:
                                
                              
                                pSoc.send(bytes("90",'utf8'))

                                countPsheetCalc=0
                            pData=b'' 
 
                        if(str(pData)[2:5]=="PIX"):
                            print("pData")
                            inputData=str(pData)[16:len(str(pData))]                            
                            dx1=float(inputData[0:10])
                            dy1=float(inputData[14:24])
                            dx2=float(inputData[28:38])
                            dy2=float(inputData[42:52])
                                                    
                            print("dx1,dy1,dx2,dy2",dx1,dy1,dx2,dy2)
                            pix11=round(sqrt(dx1**2+dy1**2),3)
                            pix12=round(sqrt(dx2**2+dy2**2),3)
                            nData=b'' 
                            
                            pass
                if data == 'exit' or not data:
                    break
            except  Exception as e:
             # print('error',str(e))
              pass

        sock.close()
        print ('Connection from closed.')    
    #---自动运行
    def bAutoClick(self):  
        calcFlag=0
        nSoc.send(bytes('200,0,0,0' ,'utf8')) 
#        if autoFlag==0:
#            if camFlag==0:
#                self.bCamIniClick()
#            if serverFlag==0:      
#                self.bTCPiniClick()        
#            self.bR1runClick()
#            self.bR2runClick()
#            time.sleep(0.2)
#            pSoc.send(bytes('200,0,0,0' ,'utf8'))     
#            nSoc.send(bytes('200,0,0,0' ,'utf8')) 
#            autoFlag=1
#            self.bAuto.setStyleSheet("background-color: rgb(0, 255, 0);")
#        
#        if autoFlag==1: 
#            if camFlag==1:
#                self.bCamIniClick()
#            if serverFlag==1:      
#                self.bTCPiniClick()         
#            self.bR1stopClick()
#            self.bR2stopClick()  
#            self.bR2resetClick()              
#            autoFlag=0
#            self.bAuto.setStyleSheet("background-color: rgb(0, 255, 0);")
        pass
    #---重置数据
    def bDataResetClick(self): 
        global countPsheetFail,countNsheetFail,countPplateFail,countNplateFail
        global countPsheetOK,countPsheetNG,countNsheetOK,countNsheetNG,countPplateOK,countPplateNG,countNplateOK,countNplateNG
        currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.tTime.setText(currentTime)
        
        self.tPsheetTotal.setText('0')
        self.tPsheetGood.setText('0')
        self.tPsheetGoodRate.setText('0')
        self.tPsheetBad.setText('0')
        self.tPsheetBadRate.setText('0')
        self.tPsheetFail.setText('0')
        
        self.tPplateTotal.setText('0')
        self.tPplateGood.setText('0')
        self.tPplateGoodRate.setText('0')
        self.tPplateBad.setText('0')
        self.tPplateBadRate.setText('0')
        self.tPplateFail.setText('0')
        
        self.tNsheetTotal.setText('0')
        self.tNsheetGood.setText('0')
        self.tNsheetGoodRate.setText('0')
        self.tNsheetBad.setText('0')
        self.tNsheetBadRate.setText('0')
        self.tNsheetFail.setText('0')
        
        self.tNplateTotal.setText('0')
        self.tNplateGood.setText('0')
        self.tNplateGoodRate.setText('0')
        self.tNplateBad.setText('0')
        self.tNplateBadRate.setText('0')
        self.tNplateFail.setText('0')
        
        countPsheetFail=0
        countNsheetFail=0
        countPplateFail=0
        countNplateFail=0
        countPsheetOK=0
        countPsheetNG=0
        countNsheetOK=0
        countNsheetNG=0
        countPplateOK=0
        countPplateNG=0
        countNplateOK=0
        countNplateNG=0
        self.outDebug("统计信息重置")  
    #---保存数据
    def bDataSaveClick(self): 
        global paraName, conn,cursor,dictPara
        dictPara['tPsheetTotal']=self.tPsheetTotal.toPlainText()
        dictPara['tPsheetGood']=self.tPsheetGood.toPlainText()
        dictPara['tPsheetGoodRate']=self.tPsheetGoodRate.toPlainText()
        dictPara['tPsheetBad']=self.tPsheetBad.toPlainText()
        dictPara['tPsheetBadRate']=self.tPsheetBadRate.toPlainText()
        dictPara['tPsheetFail']=self.tPsheetFail.toPlainText()
        dictPara['tPplateTotal']=self.tPplateTotal.toPlainText()
        dictPara['tPplateGood']=self.tPplateGood.toPlainText()
        dictPara['tPplateGoodRate']=self.tPplateGoodRate.toPlainText()        
        dictPara['tPplateBad']=self.tPplateBad.toPlainText()        
        dictPara['tPplateBadRate']=self.tPplateBadRate.toPlainText()
        dictPara['tPplateFail']=self.tPplateFail.toPlainText()
        dictPara['tNsheetTotal']=self.tNsheetTotal.toPlainText()
        dictPara['tNsheetGood']=self.tNsheetGood.toPlainText()
        dictPara['tNsheetGoodRate']=self.tNsheetGoodRate.toPlainText()
        dictPara['tNsheetBad']=self.tNsheetBad.toPlainText()
        dictPara['tNsheetBadRate']=self.tNsheetBadRate.toPlainText()
        dictPara['tNsheetFail']=self.tNsheetFail.toPlainText()
        dictPara['tNplateTotal']=self.tNplateTotal.toPlainText()
        dictPara['tNplateGood']=self.tNplateGood.toPlainText()
        dictPara['tNplateGoodRate']=self.tNplateGoodRate.toPlainText()
        dictPara['tNplateBad']=self.tNplateBad.toPlainText()
        dictPara['tNplateBadRate']=self.tNplateBadRate.toPlainText()
        dictPara['tNplateFail']=self.tNplateFail.toPlainText()
        dictPara['tTime']=self.tTime.toPlainText()
        
        dictPara['tPsheetSn']=self.tPsheetSn.toPlainText()
        dictPara['tNsheetSn']=self.tNsheetSn.toPlainText()
        dictPara['tPplateSn']=self.tPplateSn.toPlainText()                 
        dictPara['tNplateSn']=self.tNplateSn.toPlainText() 
        
        dictPara['tPip']=self.tPip.toPlainText()
        dictPara['tNip']=self.tNip.toPlainText()                 
        dictPara['tTCPport']=self.tTCPport.toPlainText()
        dictPara['tIP']=self.tIP.toPlainText()
        
        dictPara['tPsheetStandX']=self.tPsheetStandX.toPlainText()
        dictPara['tPsheetStandY']=self.tPsheetStandY.toPlainText()
        dictPara['tPsheetBadValue']=self.tPsheetBadValue.toPlainText()
        dictPara['tPsheetBadDegreeValue']=self.tPsheetBadDegreeValue.toPlainText()
        dictPara['tPsheetStandR']=self.tPsheetStandR.toPlainText()
        dictPara['tPsheetOffsetR']=self.tPsheetOffsetR.toPlainText()
        dictPara['tPsheetStandD']=self.tPsheetStandD.toPlainText()
        dictPara['tPsheetPixMM']=self.tPsheetPixMM.toPlainText()

        dictPara['tPplateStandX']=self.tPplateStandX.toPlainText()
        dictPara['tPplateStandY']=self.tPplateStandY.toPlainText()
        dictPara['tPplateBadValue']=self.tPplateBadValue.toPlainText()
        dictPara['tPplateBadDegreeValue']=self.tPplateBadDegreeValue.toPlainText()
        dictPara['tPplateStandR']=self.tPplateStandR.toPlainText()
        dictPara['tPplateOffsetR']=self.tPplateOffsetR.toPlainText()
        dictPara['tPplateStandD']=self.tPplateStandD.toPlainText() 
        dictPara['tPplatePixMM']=self.tPplatePixMM.toPlainText()
                                         
        dictPara['tNsheetStandX']=self.tNsheetStandX.toPlainText()
        dictPara['tNsheetStandY']=self.tNsheetStandY.toPlainText()
        dictPara['tNsheetBadValue']=self.tNsheetBadValue.toPlainText()
        dictPara['tNsheetBadDegreeValue']=self.tNsheetBadDegreeValue.toPlainText()
        dictPara['tNsheetStandR']=self.tNsheetStandR.toPlainText()
        dictPara['tNsheetOffsetR']=self.tNsheetOffsetR.toPlainText()
        dictPara['tNsheetStandD']=self.tNsheetStandD.toPlainText()         
        dictPara['tNsheetPixMM']=self.tNsheetPixMM.toPlainText()
                        
        dictPara['tNplateStandX']=self.tNplateStandX.toPlainText()
        dictPara['tNplateStandY']=self.tNplateStandY.toPlainText()
        dictPara['tNplateBadValue']=self.tNplateBadValue.toPlainText()  
        dictPara['tNplateBadDegreeValue']=self.tNplateBadDegreeValue.toPlainText()        
        dictPara['tNplateStandR']=self.tNplateStandR.toPlainText()
        dictPara['tNplateOffsetR']=self.tNplateOffsetR.toPlainText()
        dictPara['tNplateStandD']=self.tNplateStandD.toPlainText()          
        dictPara['tNplatePixMM']=self.tNplatePixMM.toPlainText()  
              
        dictPara['tNGpath']=self.tNGpath.toPlainText()  
        
        dictPara['tExposureTimeRawPsheet']=self.tExposureTimeRawPsheet.toPlainText() 
        dictPara['tExposureTimeRawPplate']=self.tExposureTimeRawPplate.toPlainText() 
        dictPara['tExposureTimeRawNsheet']=self.tExposureTimeRawNsheet.toPlainText() 
        dictPara['tExposureTimeRawNplate']=self.tExposureTimeRawNplate.toPlainText() 
        
        
       # print(dictPara)
        for key in dictPara:
            cursor.execute("update para set data=? where name = ?",(dictPara[key],key,))        
        conn.commit()
        self.outDebug("系统参数保存")
       # b=win32api.MessageBox(0, "保存成功", "参数保存",win32con.MB_OK)
        
    #---robot1     
    def bR1runClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK)  
            return 0
        try:
            self.rServer(1,1)     
            self.rRunMain(1)
            self.rRunComm(1)
            self.bR1run.setStyleSheet("background-color: rgb(0, 255, 0);")
        except Exception as e:
            self.statusBar().showMessage(str(e))
        pass 
    
    def bR1stopClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK) 
            return 0
        try:           
            self.rStop(1)
            self.bR1run.setStyleSheet("background-color: rgb(255, 0, 0);")
        except Exception as e:
            self.statusBar().showMessage(str(e))            
        pass
    
    def bR1resetClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK) 
            return 0
        try:           
            self.rReset(1)
            self.bR1run.setStyleSheet("background-color: rgb(192, 192, 192);")  
        except Exception as e:
            self.statusBar().showMessage(str(e))            
        pass        
   
    def bR1serverClick(self): 
        global ctrMelfaRxM
        global r1SVflage
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK)         
            return 0
        if r1SVflage==0:
            try:           
                self.rServer(1,1)
                self.bR1server.setStyleSheet("background-color: rgb(0, 255, 0);")
                r1SVflage=1
                return 0
            except Exception as e:
                self.statusBar().showMessage(str(e))         
        if r1SVflage==1:
            try:           
                self.rServer(1,0)
                self.bR1server.setStyleSheet("background-color: rgb(255, 0, 0);")
                r1SVflage=0
                return 0
            except Exception as e:
                self.statusBar().showMessage(str(e))                

    
    #---robot2    
    def bR2runClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK) 
            return 0
        try:
            self.rServer(2,1)     
            self.rRunMain(2)
            self.rRunComm(2)
            self.bR2run.setStyleSheet("background-color: rgb(0, 255, 0);")
        except Exception as e:
            self.statusBar().showMessage(str(e))
        pass 
    
    def bR2stopClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK) 
            return 0
        try:           
            self.rStop(2)
            self.bR2run.setStyleSheet("background-color: rgb(255, 0, 0);")
        except Exception as e:
            self.statusBar().showMessage(str(e))            
        pass
    
    def bR2resetClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK)
            return 0
        try:           
            self.rReset(2)
            self.bR2run.setStyleSheet("background-color: rgb(192, 192, 192);")  
        except Exception as e:
            self.statusBar().showMessage(str(e))            
        pass        
   
    def bR2serverClick(self):        
        global r2SVflage,ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            b=win32api.MessageBox(0, "机器人服务器已经关闭", "警告",win32con.MB_OK)
            return 0
        if r2SVflage==0:
            try:           
                self.rServer(2,1)
                self.bR2server.setStyleSheet("background-color: rgb(0, 255, 0);")
                r2SVflage=1
                return 0
            except Exception as e:
                self.statusBar().showMessage(str(e))         
        if r2SVflage==1:
            try:           
                self.rServer(2,0)
                self.bR2server.setStyleSheet("background-color: rgb(255, 0, 0);")
                r2SVflage=0
                return 0
            except Exception as e:
                self.statusBar().showMessage(str(e)) 
    
    def bRreconnectClick(self):
        global ctrMelfaRxM
        if ctrMelfaRxM.ServerLive()==False:
            ctrMelfaRxM.ServerStart()   
            
    def bRconnectOffClick(self):
        global ctrMelfaRxM
        try:
            self.bR1stopClick()
            self.bR2stopClick()
        except:
            pass
        try:
            ctrMelfaRxM.ServerKill()  
        except:
            pass            
            
            
            
#---检测设定界面，按钮事件    
    def bSelectDocClick(self):  
        directory1 = QFileDialog.getExistingDirectory(self,  "选取文件夹",  "D:/") #起始路径  
        self.tNGpath.setText(directory1) 
        self.outDebug("修改NG文件夹:"+directory1)
#        print(directory1)
#        img1=cv2.imread("arrayBmp0.bmp")
#        cv2.imwrite(directory1+"/arrayBmp3.bmp",img1) 
    
#---机器人手动界面，按钮事件      
    #---位置数据保存按钮
    def bR1saveClick(self): 
        self.rWritePosition(1)
        pass
    def bR2saveClick(self): 
        self.rWritePosition(2)
        pass

    #---手动走位按钮1
    def bR1Mgo1Click(self): 
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp1.placeholderText()]+","+self.tR1Mspeed.toPlainText() ,'utf8'))  
        time.sleep(0.2)
    def bR1Mgo2Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp2.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8'))  
        time.sleep(0.2)
    def bR1Mgo3Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp3.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.2)
    def bR1Mgo4Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp4.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8')) 
        time.sleep(0.2)
    def bR1Mgo5Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp5.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8'))   
        time.sleep(0.2)
    def bR1Mgo6Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp6.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.2)
    def bR1Mgo7Click(self):
        global MposiontCodDic
        pSoc.send(bytes(MposiontCodDic[self.tMp7.placeholderText()]+","+self.tR1Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.2)
    def bR1Mio1Click(self):
        global R1Do1_ON
        if R1Do1_ON==0:
            pSoc.send(bytes('504,0,0,0' ,'utf8')) 
            self.bR1Mio1.setStyleSheet("background-color: rgb(0, 255, 0);")
            R1Do1_ON=1
            return 0
        if R1Do1_ON==1:
            pSoc.send(bytes('505,0,0,0' ,'utf8'))   
            R1Do1_ON=0
            self.bR1Mio1.setStyleSheet("background-color: rgb(255, 0, 0);")
            return 0
    def bR1Mio2Click(self):
        global R1Do2_ON
        if R1Do2_ON==0:
            pSoc.send(bytes('506,0,0,0' ,'utf8')) 
            self.bR1Mio2.setStyleSheet("background-color: rgb(0, 255, 0);")
            R1Do2_ON=1
            return 0
        if R1Do2_ON==1:
            pSoc.send(bytes('507,0,0,0' ,'utf8'))   
            R1Do2_ON=0
            self.bR1Mio2.setStyleSheet("background-color: rgb(255, 0, 0);")
            return 0       
                                                        
    #---R1手动位置设置  
    def bR1Mgo1SetClick(self):     
        pSoc.send(bytes('503,0,0,0' ,'utf8'))  
        time.sleep(0.5)
        pass
    
    def bR1Mgo2SetClick(self):     
        pSoc.send(bytes('500,0,0,0' ,'utf8'))  
        time.sleep(0.5)     
        pass        
    
    def bR1Mgo3SetClick(self):     
        pSoc.send(bytes('502,0,0,0' ,'utf8'))    
        time.sleep(0.5)   
        pass        
    
    def bR1Mgo4SetClick(self):     
        pSoc.send(bytes('501,0,0,0' ,'utf8'))   
        time.sleep(0.5)
        pass          
    
    def bR1Mgo5SetClick(self):           
        pass   
    def bR1Mgo6SetClick(self):           
        pass 
    def bR1Mgo7SetClick(self):           
        pass       
    #---点动按钮1  
    def bR1XPgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("300,"+self.tR1Mspeed.toPlainText()+","+self.tR1Mdistance.toPlainText(),'utf8'))  
        time.sleep(0.2)
    def bR1XNgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("300,"+self.tR1Mspeed.toPlainText()+",-"+self.tR1Mdistance.toPlainText(),'utf8'))            
        time.sleep(0.2)
    def bR1YPgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("301,"+self.tR1Mspeed.toPlainText()+","+self.tR1Mdistance.toPlainText(),'utf8'))          
        
    def bR1YNgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("301,"+self.tR1Mspeed.toPlainText()+",-"+self.tR1Mdistance.toPlainText(),'utf8'))              
        time.sleep(0.2)
    def bR1ZPgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("302,"+self.tR1Mspeed.toPlainText()+","+self.tR1Mdistance.toPlainText(),'utf8'))           
        time.sleep(0.2)
    def bR1ZNgoClick(self):
        global MposiontCodDic
        pSoc.send(bytes("302,"+self.tR1Mspeed.toPlainText()+",-"+self.tR1Mdistance.toPlainText(),'utf8'))  
        time.sleep(0.2)      
    def bR1CPgoClick(self):
        global MposiontCodDic
        deg=str(float(self.tR1Mdistance.toPlainText())*3.14/180)
        print("deg:",deg)
        pSoc.send(bytes("303,"+self.tR1Mspeed.toPlainText()+","+deg,'utf8'))           
        time.sleep(0.2)
    def bR1CNgoClick(self):
        global MposiontCodDic
        deg=str(float(self.tR1Mdistance.toPlainText())*3.14/180)
        
        print("deg:",deg)
        pSoc.send(bytes("303,"+self.tR1Mspeed.toPlainText()+",-"+deg,'utf8')) 
        time.sleep(0.2)
    #---手动走位按钮2
    def bR2Mgo1Click(self): 
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp1.placeholderText()]+","+self.tR2Mspeed.toPlainText() ,'utf8'))  
        time.sleep(0.5)
    def bR2Mgo2Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp2.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8'))  
        time.sleep(0.5)
    def bR2Mgo3Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp3.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.5)
    def bR2Mgo4Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp4.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8')) 
        time.sleep(0.5)
    def bR2Mgo5Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp5.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8'))   
        time.sleep(0.5)
    def bR2Mgo6Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp6.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.5)
    def bR2Mgo7Click(self):
        global MposiontCodDic
        nSoc.send(bytes(MposiontCodDic[self.tR2Mp7.placeholderText()]+","+self.tR2Mspeed.toPlainText(),'utf8'))          
        time.sleep(0.5)
        
    def bR2Mio1Click(self):
        global R2Do1_ON
        if R2Do1_ON==0:
            nSoc.send(bytes('504,0,0,0' ,'utf8')) 
            self.bR2Mio1.setStyleSheet("background-color: rgb(0, 255, 0);")
            R2Do1_ON=1
            return 0
        if R2Do1_ON==1:
            nSoc.send(bytes('505,0,0,0' ,'utf8'))   
            R2Do1_ON=0
            self.bR2Mio1.setStyleSheet("background-color: rgb(255, 0, 0);")
            return 0
    def bR2Mio2Click(self):
        global R2Do2_ON
        if R2Do2_ON==0:
            nSoc.send(bytes('506,0,0,0' ,'utf8')) 
            self.bR2Mio2.setStyleSheet("background-color: rgb(0, 255, 0);")
            R2Do2_ON=1
            return 0
        if R2Do2_ON==1:
            nSoc.send(bytes('507,0,0,0' ,'utf8'))   
            R2Do2_ON=0
            self.bR2Mio2.setStyleSheet("background-color: rgb(255, 0, 0);")
            return 0          
        
        
        
        
        
        
    #---r2手动位置设置          
    def bR2Mgo1SetClick(self):     
        nSoc.send(bytes('503,0,0,0' ,'utf8'))
        time.sleep(0.5)          
        pass
    def bR2Mgo2SetClick(self):     
        nSoc.send(bytes('500,0,0,0' ,'utf8'))  
        time.sleep(0.5)        
        pass        
    def bR2Mgo3SetClick(self):     
        nSoc.send(bytes('502,0,0,0' ,'utf8'))
        time.sleep(0.5)
        pass        
    def bR2Mgo4SetClick(self):     
        nSoc.send(bytes('501,0,0,0' ,'utf8'))
        time.sleep(0.5)        
        pass          
    def bR2Mgo5SetClick(self):           
        pass   
    def bR2Mgo6SetClick(self):           
        pass 
    def bR2Mgo7SetClick(self):           
        pass
                       
    #---点动按钮2    
    def bR2XPgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("300,"+self.tR2Mspeed.toPlainText()+","+self.tR2Mdistance.toPlainText(),'utf8'))  
        time.sleep(0.5)
    def bR2XNgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("300,"+self.tR2Mspeed.toPlainText()+",-"+self.tR2Mdistance.toPlainText(),'utf8'))            
        time.sleep(0.5)
    def bR2YPgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("301,"+self.tR2Mspeed.toPlainText()+","+self.tR2Mdistance.toPlainText(),'utf8'))          
        time.sleep(0.5)      
    def bR2YNgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("301,"+self.tR2Mspeed.toPlainText()+",-"+self.tR2Mdistance.toPlainText(),'utf8'))              
        time.sleep(0.5)
    def bR2ZPgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("302,"+self.tR2Mspeed.toPlainText()+","+self.tR2Mdistance.toPlainText(),'utf8'))           
        time.sleep(0.5)
    def bR2ZNgoClick(self):
        global MposiontCodDic
        nSoc.send(bytes("302,"+self.tR2Mspeed.toPlainText()+",-"+self.tR2Mdistance.toPlainText(),'utf8'))  
        time.sleep(0.5)      
    def bR2CPgoClick(self):
        global MposiontCodDic
        deg=str(float(self.tR2Mdistance.toPlainText())*3.14/180)
        print("deg:",deg)
        nSoc.send(bytes("303,"+self.tR2Mspeed.toPlainText()+","+deg,'utf8'))           
        time.sleep(0.5)
    def bR2CNgoClick(self):
        global MposiontCodDic
        deg=str(float(self.tR2Mdistance.toPlainText())*3.14/180)
        
        print("deg:",deg)
        nSoc.send(bytes("303,"+self.tR2Mspeed.toPlainText()+",-"+deg,'utf8'))
        time.sleep(0.5)
#---视觉调试界面按钮事件

    #---R1坐标标定位置数据设置  
    def bR1SetPT31Click(self):     
        pSoc.send(bytes('521,0,0,0' ,'utf8'))  
        pass
    def bR1SetPT32Click(self):     
        pSoc.send(bytes('522,0,0,0' ,'utf8'))  
        pass
    def bR1SetPT33Click(self):     
        pSoc.send(bytes('523,0,0,0' ,'utf8'))  
        pass  
    def bR1SetPT21Click(self):     
        pSoc.send(bytes('511,0,0,0' ,'utf8'))  
        pass
    def bR1SetPT22Click(self):     
        pSoc.send(bytes('512,0,0,0' ,'utf8'))  
        pass
    def bR1SetPT23Click(self):     
        pSoc.send(bytes('513,0,0,0' ,'utf8'))  
        pass    
    
    
    
    #---R2坐标标定位置数据设置 
    def bR2SetPT31Click(self):     
        nSoc.send(bytes('521,0,0,0' ,'utf8'))  
        pass
    def bR2SetPT32Click(self):     
        nSoc.send(bytes('522,0,0,0' ,'utf8'))  
        pass
    def bR2SetPT33Click(self):     
        nSoc.send(bytes('523,0,0,0' ,'utf8'))  
        pass  
    def bR2SetPT21Click(self):     
        nSoc.send(bytes('511,0,0,0' ,'utf8'))  
        pass
    def bR2SetPT22Click(self):     
        nSoc.send(bytes('512,0,0,0' ,'utf8'))  
        pass
    def bR2SetPT23Click(self):     
        nSoc.send(bytes('513,0,0,0' ,'utf8'))  
        pass               
    
    def radioCalcClick(self):
        global calcFlag
        if self.radioCalc.isChecked(): 
            calcFlag=1
        else:
            calcFlag=0
        pass

    #---位置组合标定  
    def bPpostionCalclick(self):
        calcFlag=0
        pSoc.send(bytes('1000,0,0,0' ,'utf8'))  
        pass

    def bNpostionCalclick(self):
        calcFlag=0
        nSoc.send(bytes('1000,0,0,0' ,'utf8'))  
        pass



    #---实时线程  
    def bRealTimePsheetThread(self):
        while True:
            time.sleep(0.3)   
            self.bPsheetTrigClick()
            print("done1")
            
    def bRealTimePplateThread(self):
        while True:
            time.sleep(0.3)   
            self.bPplateTrigClick()
            print("done2")
            
    def bRealTimeNsheetThread(self):
        while True:
            time.sleep(0.3)   
            self.bNsheetTrigClick()
            print("done3")
            
    def bRealTimeNplateThread(self):
        while True:
            time.sleep(0.3)   
            self.bNplateTrigClick()
            print("done4")
            
    #---实时按钮           
    def bRealTimePsheetClick(self):
        global pSheetRealTimeFlag ,trig1
        if pSheetRealTimeFlag==0:
            trig1 = threading.Thread(target=self.bRealTimePsheetThread) 
            trig1.start()   
            pSheetRealTimeFlag=1
            self.bRealTimePsheet.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            try:
                self.stop_thread(trig1)  
            except:
                pass
            pSheetRealTimeFlag=0
            self.bRealTimePsheet.setStyleSheet("background-color: rgb(255, 0, 0);")
        pass
    
    def bRealTimePplateClick(self):
        global pPlateRealTimeFlag ,trig2
        if pPlateRealTimeFlag==0:
            trig2 = threading.Thread(target=self.bRealTimePplateThread) 

            trig2.start()   
            pPlateRealTimeFlag=1
            self.bRealTimePplate.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            try:
                self.stop_thread(trig2)  
            except:
                pass
            pPlateRealTimeFlag=0
            self.bRealTimePplate.setStyleSheet("background-color: rgb(255, 0, 0);")
        pass        
    
    def bRealTimeNsheetClick(self):
        global nSheetRealTimeFlag ,trig3
        if nSheetRealTimeFlag==0:
            trig3 = threading.Thread(target=self.bRealTimeNsheetThread) 

            trig3.start()   
            nSheetRealTimeFlag=1
            self.bRealTimeNsheet.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            try:
                self.stop_thread(trig3)  
            except:
                pass
            nSheetRealTimeFlag=0
            self.bRealTimeNsheet.setStyleSheet("background-color: rgb(255, 0, 0);")
        pass
    
    def bRealTimeNplateClick(self):
        global nPlateRealTimeFlag ,trig4
        if nPlateRealTimeFlag==0:
            trig4 = threading.Thread(target=self.bRealTimeNplateThread) 

            trig4.start()   
            nPlateRealTimeFlag=1
            self.bRealTimeNplate.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            try:
                self.stop_thread(trig4)  
            except:
                pass
            nPlateRealTimeFlag=0
            self.bRealTimeNplate.setStyleSheet("background-color: rgb(255, 0, 0);")
        pass    

#    def CapThread(self,camNum,window):       
#       while True:
#            time.sleep(0.3)
#            self.capBmp(camNum)            
#            print("cap0 done")
#            img1=cv2.imread("Bmp0.bmp")
#            imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)        
#            cv2.line(imgray,(0,972), (2592,972), (0,0,255),2)
#            cv2.line(imgray,(1296,0), (1296,1944), (0,0,255),2)
#            self.lCamSheetP_2.setPixmap(self.toPixImg(imgray))
    
    #---工具标定按钮                
    
    def bPsheetToolCalcClick(self):
        global pSheetToolFlag , pSheetRealTimeFlag   
        if pSheetRealTimeFlag==0:  
            self.bRealTimePsheetClick()        
        if pSheetToolFlag==0:
            try:
                pSoc.send(bytes('120,0,0,0' ,'utf8'))             
                pSheetToolFlag=1
                self.bPsheetToolCalc.setStyleSheet("background-color: rgb(0, 255, 0);")
                self.bPsheetToolCalcNext.show()
            except Exception as e:
                self.statusBar().showMessage(str(e))                
        else:
            pSheetToolFlag=0
            self.bPsheetToolCalc.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.bPsheetToolCalcNext.hide()
        pass
    
    def bPsheetToolCalcNextClick(self):
        global pSheetToolNextFlag,pSheetToolFlag
        if pSheetToolNextFlag==0:
            try:
                pSoc.send(bytes('121,0,0,0' ,'utf8')) 
                pSheetToolNextFlag=1
                self.bPsheetToolCalcNext.setStyleSheet("background-color: rgb(255, 150, 240);")                
            except Exception as e:
                self.statusBar().showMessage(str(e))
            return 0
        if pSheetToolNextFlag==1:
            pSoc.send(bytes('122,0,0,0' ,'utf8')) 
            pSheetToolNextFlag=0
            self.bPsheetToolCalcNext.setStyleSheet("background-color: rgb(150, 150, 240);")
            b=win32api.MessageBox(0, "标定完成", "工具坐标标定",win32con.MB_OK) 
            self.bPsheetToolCalcNext.hide()    
            self.bPsheetToolCalc.setStyleSheet("background-color: rgb(255, 255, 240);")
            pSheetToolFlag=0
            return 0
        pass    
    
                
    def bPplateToolCalcClick(self):
        global bPplateToolFlag,pPlateRealTimeFlag  
        if pPlateRealTimeFlag==0:  
            self.bRealTimePplateClick()                       
        if bPplateToolFlag==0:
            win32api.MessageBox(0, "请确认相机底下无盖板", "工具坐标标定",win32con.MB_OK) 
            pSoc.send(bytes('100,0,0,0' ,'utf8')) 
            bPplateToolFlag=1
            self.bPplateToolCalc.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.bPplateToolCalcNext.show()
        else:
            
            bPplateToolFlag=0
            self.bPplateToolCalc.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.bPplateToolCalcNext.hide()        
        pass  
    
    def bPplateToolCalcNextClick(self):
        global bPplateToolNextFlag,bPplateToolFlag
       
        if bPplateToolNextFlag==0:
            pSoc.send(bytes('110,0,0,0' ,'utf8')) 
            bPplateToolNextFlag=1
            self.bPplateToolCalcNext.setStyleSheet("background-color: rgb(255, 150, 240);")
            return 0
        if bPplateToolNextFlag==1:
            pSoc.send(bytes('111,0,0,0' ,'utf8')) 
            bPplateToolNextFlag=0
            self.bPplateToolCalcNext.setStyleSheet("background-color: rgb(150, 150, 240);")
            b=win32api.MessageBox(0, "标定完成", "工具坐标标定",win32con.MB_OK) 
            self.bPplateToolCalcNext.hide()    
            self.bPplateToolCalc.setStyleSheet("background-color: rgb(255, 255, 240);")
            bPplateToolFlag=0
            return 0
        pass        
    def bNsheetToolCalcClick(self):
        global nSheetToolFlag ,nSheetRealTimeFlag
        if nSheetRealTimeFlag==0:  
            self.bRealTimeNsheetClick()
        if nSheetToolFlag==0:
            try:
                nSoc.send(bytes('120,0,0,0' ,'utf8'))             
                nSheetToolFlag=1
                self.bNsheetToolCalc.setStyleSheet("background-color: rgb(0, 255, 0);")
                self.bNsheetToolCalcNext.show()
            except Exception as e:
                self.statusBar().showMessage(str(e))                
        else:
            nSheetToolFlag=0
            self.bNsheetToolCalc.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.bNsheetToolCalcNext.hide()
        pass
    
    def bNsheetToolCalcNextClick(self):
        global nSheetToolNextFlag,nSheetToolFlag
        if nSheetToolNextFlag==0:
            try:
                nSoc.send(bytes('121,0,0,0' ,'utf8')) 
                nSheetToolNextFlag=1
                self.bNsheetToolCalcNext.setStyleSheet("background-color: rgb(255, 150, 240);")                
            except Exception as e:
                self.statusBar().showMessage(str(e))
            return 0
        if nSheetToolNextFlag==1:
            nSoc.send(bytes('122,0,0,0' ,'utf8')) 
            nSheetToolNextFlag=0
            self.bNsheetToolCalcNext.setStyleSheet("background-color: rgb(150, 150, 240);")
            b=win32api.MessageBox(0, "标定完成", "工具坐标标定",win32con.MB_OK) 
            self.bNsheetToolCalcNext.hide()    
            self.bNsheetToolCalc.setStyleSheet("background-color: rgb(255, 255, 240);")
            nSheetToolFlag=0
            return 0
        pass    
    
                
    def bNplateToolCalcClick(self):
        global bNplateToolFlag,nPlateRealTimeFlag  
        if nPlateRealTimeFlag==0:  
            self.bRealTimeNplateClick()                       
        if bNplateToolFlag==0:
            win32api.MessageBox(0, "请确认相机底下无盖板", "工具坐标标定",win32con.MB_OK) 
            nSoc.send(bytes('100,0,0,0' ,'utf8')) 
            bNplateToolFlag=1
            self.bNplateToolCalc.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.bNplateToolCalcNext.show()
        else:
            bNplateToolFlag=0
            self.bNplateToolCalc.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.bNplateToolCalcNext.hide()        
        pass  
    
    def bNplateToolCalcNextClick(self):
        global bNplateToolNextFlag,bNplateToolFlag
        if bNplateToolNextFlag==0:
            nSoc.send(bytes('110,0,0,0' ,'utf8')) 
            bNplateToolNextFlag=1
            self.bNplateToolCalcNext.setStyleSheet("background-color: rgb(255, 150, 240);")
            return 0
        if bNplateToolNextFlag==1:
            nSoc.send(bytes('111,0,0,0' ,'utf8')) 
            bNplateToolNextFlag=0
            self.bNplateToolCalcNext.setStyleSheet("background-color: rgb(150, 150, 240);")
            b=win32api.MessageBox(0, "标定完成", "工具坐标标定",win32con.MB_OK) 
            self.bNplateToolCalcNext.hide()    
            self.bNplateToolCalc.setStyleSheet("background-color: rgb(255, 255, 240);")
            bNplateToolFlag=0
            return 0
        pass     
    

    #---坐标标定按钮
    def bPsheetCalcClick(self):
        global nData,pData,nSoc,pSoc ,serverFlag,serverSoc,tn,tp,pSheetCalcDone,countPsheetCalc,pCalcFlag,pSheetRealTimeFlag,calcFlag
        pSheetCalcDone=0
        countPsheetCalc=0
        calcFlag=1
        print("serverFlag:",serverFlag)
        if pSheetRealTimeFlag==1:
            self.bRealTimePsheetClick()
        if serverFlag==1:
            try:
                pSoc.send(bytes("401",'utf8'))
                pCalcFlag=1
            except Exception as e:
                print(str(e))

    def bPplateCalcClick(self):
        global nData,pData,nSoc,pSoc ,serverFlag,serverSoc,tn,tp,pSheetCalcDone,countPsheetCalc,pPlateRealTimeFlag,calcFlag
        pSheetCalcDone=0
        countPsheetCalc=0
        calcFlag=1
        print("serverFlag:",serverFlag)
        if pPlateRealTimeFlag==1:
            self.bRealTimePplateClick()
        if serverFlag==1:
            try:
                pSoc.send(bytes("400",'utf8'))
            except Exception as e:
                print(str(e))       
                
    def bNsheetCalcClick(self):
        global nData,pData,nSoc,pSoc ,serverFlag,serverSoc,tn,tp,nSheetCalcDone,countNsheetCalc,nCalcFlag,nSheetRealTimeFlag,calcFlag
        nSheetCalcDone=0
        countNsheetCalc=0
        calcFlag=1
        print("serverFlag:",serverFlag)
        if nSheetRealTimeFlag==1:
            self.bRealTimeNsheetClick()        
        if serverFlag==1:
            try:
                nSoc.send(bytes("401",'utf8'))
                nCalcFlag=1
            except Exception as e:
                print(str(e))
                
    def bNplateCalcClick(self):
        global nData,pData,nSoc,pSoc ,serverFlag,serverSoc,tn,tp,nSheetCalcDone,countNsheetCalc,nPlateRealTimeFlag,calcFlag
        nSheetCalcDone=0
        countNsheetCalc=0
        print("serverFlag:",serverFlag)
        if nPlateRealTimeFlag==1:
            self.bRealTimeNplateClick()
        if serverFlag==1:
            try:
                nSoc.send(bytes("400",'utf8'))
            except Exception as e:
                print(str(e))   

    def bPsheetUpdateTableClick(self):
        global tablePs
        for j in range(9):
            for i in range(4):
                newItem=QTableWidgetItem(tablePs[i][j])
                self.tableWidgetPs.setItem(j,i,newItem) 
        self.xmlCalcUpdate("calc1.ccc",tablePs,0)            
    def bPplateUpdateTableClick(self):
        global tablePs
        for j in range(9):
            for i in range(4):
                newItem=QTableWidgetItem(tablePs[i][j])
                self.tableWidgetPp.setItem(j,i,newItem)
        self.xmlCalcUpdate("calc1.ccc",tablePs,1)
                
    def bNsheetUpdateTableClick(self):
        global tableNs
        for j in range(9):
            for i in range(4):
                newItem=QTableWidgetItem(tableNs[i][j])
                self.tableWidgetNs.setItem(j,i,newItem) 
        self.xmlCalcUpdate("calc1.ccc",tableNs,0)

    def bNplateUpdateTableClick(self):
        global tableNs
        for j in range(9):
            for i in range(4):
                newItem=QTableWidgetItem(tableNs[i][j])
                self.tableWidgetNp.setItem(j,i,newItem)   
        self.xmlCalcUpdate("calc1.ccc",tableNs,1)
                
    #---更新曝光时间                 
    def bUpdateCamClick(self):
        global camera,exposCalc,expos,exposDic,snDic
        expos=[int(self.tExposureTimeRawPsheet.toPlainText()),int(self.tExposureTimeRawPplate.toPlainText()),int(self.tExposureTimeRawNsheet.toPlainText()),int(self.tExposureTimeRawNplate.toPlainText()) ]
        exposCalc=[max(35,min(int(expos[i]/35)*35,999985)) for i in range(len(expos))] 
        exposDic={"pSheet":exposCalc[0],"pPlate":exposCalc[1],"nSheet":exposCalc[2],"nPlate":exposCalc[3]}
        for i in range(len(camera)):
            deviceID=camera[i].Parameters[PLCamera.DeviceID].GetValue()
            print(deviceID) 
            camera[i].Parameters[PLCamera.ExposureTimeRaw].SetValue(exposDic[snDic[deviceID]])
            print(exposDic[snDic[deviceID]])           

    #---相机触发
    #file="Bmp0.bmp"
    #camNum=0
    #camName="pSheet"
    #visionStand=["tPsheetStandX","tPsheetStandY","tPsheetBadValue"]\
    #sn=self.tPsheetSn.toPlainText()
    #bTrigFunc相机触发功能函数
    def bTrigFunc(self,sn,file,camNum,camName,visionStand):
        global basler,dictPara,dictParaVision,snDic ,mod ,camFlag,pSheetToolFlag,snCalc,snStr ,pSheetRealTimeFlag
        global calcFlag,countPsheetOK,countPsheetNG,countNsheetOK,countNsheetNG,countPplateOK,countPplateNG,countNplateOK,countNplateNG
        global countPsheetFail,countNsheetFail,countPplateFail,countNplateFail
        
        s1=time.time()        
        result="NG"  
        resultLine=0
        resultCircle=0
        circle=[(0,0),0]
        line=[(0,0),(0,0),0]
        if mod==1:
            print("mod:",mod)
            if camFlag==1:            
                self.capBmp(snCalc.index(sn),camNum)           
                img1=cv2.imread(file)
                imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("array"+file,imgray)  
            else:
                b=win32api.MessageBox(0, "相机未连接，请连接相机，测试请离线", "相机未连接",win32con.MB_OK)
                return -1
        if mod==0:
            print("mod:",mod)
            img1=cv2.imread("array"+file)
            imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            
            
        e1=time.time()
        capTime="Cap time:"+str(round((e1-s1),2))                 
        #调用visionpro处理,visionpro.py
        print("calcFlag:",calcFlag)
        if calcFlag==0:
            print(resultCircle,circle,resultLine,line)
            resultCircle,circle=visionpro.simpleFindCircle(camName) 
            if resultCircle==0:
                if camNum==0:
                    countPsheetFail=countPsheetFail+1
                if camNum==1:
                    countPplateFail=countPplateFail+1        
                if camNum==2:
                    countNsheetFail=countNsheetFail+1
                if camNum==3:
                    countNplateFail=countNplateFail+1
            resultLine,line=visionpro.simpleFindLine(camName)
            print(resultCircle,circle,resultLine,line)
        if calcFlag==1:
            resultCircle,circle=visionpro.find(camName)  
            print("resultCircle,circle:",resultCircle,circle)
        e2=time.time()
        processTime="Process time:"+str(round((e2-e1),2))
        circleDefine=(abs(int(circle[0][0])-int(dictPara[visionStand[0]]))>int(dictPara[visionStand[2]]))\
        |(abs(int(circle[0][1])-int(dictPara[visionStand[1]]))>int(dictPara[visionStand[2]]))
#        |(abs(int(round(math.degrees(line[2]),2))-int(dictPara["tPsheetBadDegreeValue"]))>int(dictPara[visionStand[2]]))
        round(math.degrees(line[2]),2)
        if (circleDefine and calcFlag==0 and resultCircle==1):
            if camNum==0:
                countPsheetNG=countPsheetNG+1
            if camNum==1:
                countPplateNG=countPplateNG+1        
            if camNum==2:
                countNsheetNG=countNsheetNG+1
            if camNum==3:
                countNplateNG=countNplateNG+1
        if (circleDefine==0 and calcFlag==0 ):
            if camNum==0:
                countPsheetOK=countPsheetOK+1
            if camNum==1:
                countPplateOK=countPplateOK+1        
            if camNum==2:
                countNsheetOK=countNsheetOK+1
            if camNum==3:
                countNplateOK=countNplateOK+1                
        docName="/"+str(camNum+1)+"/"+time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time()))
        print("circleDefine:",circleDefine)
        if (resultCircle==1 and resultLine==1 and calcFlag==0) or (resultCircle==1 and calcFlag==1) :
#            self.outDebug("正极过渡片搜索成功")
            #circle[0]是圆心坐标,circle[1]是半径
            print("circle ")
            cv2.circle(img1,(int(circle[0][0]),int(circle[0][1])),int(circle[1]),(255,0,255),8)
            cv2.circle(img1,(int(circle[0][0]),int(circle[0][1])),5,(55,255,155),-1)            
            #line[0]是直线起点,line[1]是直线终点,line[2]是角度
            if calcFlag==0: 
                cv2.line(img1, (int(line[0][0]),int(line[0][1])), (int(line[1][0]),int(line[1][1])), (255,0,255),10)
            
            cv2.putText(img1,"circle:"+str(circle[0])+"offset:"+str(round(math.degrees(line[2]),2))+"deg",(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            cv2.putText(img1,capTime,(10,200),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            cv2.putText(img1,processTime,(10,300),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            
            #保存在NG文件夹的3号文件夹            
            #score["result"]==0,找到但是不满足设置条件的          
            if (circleDefine and calcFlag==0):
#                self.outDebug("正极过渡片不满足设置要求")
                cv2.rectangle(img1,(10,10),(2582,1934),(0,0,255),10)
                if self.rSize.isChecked(): 
                    res=imgray
                    docType=".bmp"
                else:
                    res=cv2.resize(imgray,(518,389),interpolation=cv2.INTER_CUBIC)
                    docType=".jpg"
                if pSheetRealTimeFlag==0:
                    cv2.imwrite(dictPara['tNGpath']+docName+docType,res)
                
                cv2.putText(img1,"NG",(1200,300),cv2.FONT_HERSHEY_COMPLEX,10,(0,0,255),10)
                if self.rSize.isChecked(): 
                    res=img1
                else:
                    res=cv2.resize(img1,(518,389),interpolation=cv2.INTER_CUBIC)
                if pSheetRealTimeFlag==0:    
                    cv2.imwrite(dictPara['tNGpath']+docName+"R"+docType,res)  
                result="NG" 
               # circle[0]=(0,0)
#           """ OK状态    找到且满足设置要求,返回给机器人                       
            else:
                #找到且满足设置要求,返回给机器人
               cv2.rectangle(img1,(10,10),(2582,1934),(55,255,155),10)
               cv2.putText(img1,"OK",(1200,300),cv2.FONT_HERSHEY_COMPLEX,10,(55,255,155),10)
               result="OK" 
               
        #score["result"]==0,分类处理                     
        else:
            cv2.putText(img1,"NG",(1200,300),cv2.FONT_HERSHEY_COMPLEX,10,(0,0,255),10)
            cv2.rectangle(img1,(10,10),(2582,1934),(0,0,255),10)
#            if score["PMA"]==0:
#                cv2.putText(img1,"Align:0",(20,200),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
#                self.outDebug("模型匹配失败")
#            else:
#                cv2.putText(img1,"Align:1",(10,200),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
#                self.outDebug("模型匹配成功")
            if resultCircle==1:
                cv2.putText(img1,"circle:"+str(circle[0]),(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
                cv2.circle(img1,(int(circle[0][0]),int(circle[0][1])),int(circle[1]),(255,0,255),8)
                self.outDebug("找到圆")
            else:
                cv2.putText(img1,"circle:0",(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
                self.outDebug("找不到圆")
            if resultLine==1:
                cv2.putText(img1,"line angle:"+str(line[2]),(10,300),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
                cv2.line(img1, (int(line[0][0]),int(line[0][1])), (int(line[1][0]),int(line[1][1])), (255,0,255),10)
                self.outDebug("找到线")
            else:
                cv2.putText(img1,"line:0",(10,300),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
                self.outDebug("找不到线") 
                       
            if self.rSize.isChecked(): 
                res=imgray
                docType=".bmp"
            else:
                res=cv2.resize(imgray,(518,389),interpolation=cv2.INTER_CUBIC)
                docType=".jpg"
            cv2.imwrite(dictPara['tNGpath']+docName+docType,res)
                
            cv2.putText(img1,"NG",(1200,300),cv2.FONT_HERSHEY_COMPLEX,10,(0,0,255),10)
            if self.rSize.isChecked(): 
                res=img1
            else:
                res=cv2.resize(img1,(518,389),interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(dictPara['tNGpath']+docName+"R"+docType,res)   
            circle[0]=(0,0)
            line[2]=0
            result="NG"  
        cv2.line(img1,(0,972), (2592,972), (0,0,255),2)
        cv2.line(img1,(1296,0), (1296,1944), (0,0,255),2)     
        if camNum==0:        
            self.lCamSheetP.setPixmap(self.toPixImg(img1))
            self.lCamSheetP_2.setPixmap(self.toPixImg(img1))   
        if camNum==1:        
            self.lCamPlateP.setPixmap(self.toPixImg(img1))
            self.lCamPlateP_2.setPixmap(self.toPixImg(img1))   
        if camNum==2:        
            self.lCamSheetN.setPixmap(self.toPixImg(img1))
            self.lCamSheetN_2.setPixmap(self.toPixImg(img1))   
        if camNum==3:        
            self.lCamPlateN.setPixmap(self.toPixImg(img1))
            self.lCamPlateN_2.setPixmap(self.toPixImg(img1))  
        if result=="NG":
            circle[0]=(0,0)                 
        return circle[0],line[2],result    
            
    def bPsheetTrigClick(self):
        global basler,dictPara,dictParaVision,snDic ,mod ,camFlag,pSheetToolFlag,snCalc,snStr ,pSheetRealTimeFlag
        file="Bmp0.bmp"
        camNum=0
        camName="pSheet"
        visionStand=["tPsheetStandX","tPsheetStandY","tPsheetBadValue"]
        sn=self.tPsheetSn.toPlainText()
        circle,line,result=self.bTrigFunc(sn,file,camNum,camName,visionStand)
        return circle,line,result

            
    def bPplateTrigClick(self):
        global basler,dictPara,dictParaVision,centPplate ,snDic ,mod,camFlag       
        file="Bmp1.bmp"
        camNum=1
        camName="pPlate"
        visionStand=["tPplateStandX","tPplateStandY","tPplateBadValue"]
        sn=self.tPplateSn.toPlainText()
        circle,line,result=self.bTrigFunc(sn,file,camNum,camName,visionStand)
        return circle,line,result
    
    def bNsheetTrigClick(self):
        global basler,dictPara,dictParaVision,snDic ,mod ,camFlag,pSheetToolFlag,snCalc,snStr ,pSheetRealTimeFlag
        file="Bmp2.bmp"
        camNum=2
        camName="nSheet"
        visionStand=["tNsheetStandX","tNsheetStandY","tNsheetBadValue"]
        sn=self.tNsheetSn.toPlainText()
        circle,line,result=self.bTrigFunc(sn,file,camNum,camName,visionStand)
        return circle,line,result
    
    def bNplateTrigClick(self):
        global basler,dictPara,dictParaVision,centPplate ,snDic ,mod,camFlag       
        file="Bmp3.bmp"
        camNum=3
        camName="nPlate"
        visionStand=["tNplateStandX","tNplateStandY","tNplateBadValue"]
        sn=self.tNplateSn.toPlainText()
        circle,line,result=self.bTrigFunc(sn,file,camNum,camName,visionStand)
        return circle,line,result   
    
#---basler相机初始化，拍照
    def camIni(self):
        global camera,exposCalc,expos,exposDic,snDic,snCalc,snStr       
        sn=[int(self.tPsheetSn.toPlainText()),int(self.tPplateSn.toPlainText()),int(self.tNsheetSn.toPlainText()),int(self.tNplateSn.toPlainText())]
        snStr=[str(i) for i in sn]
        print("sn:",sn)
        snDic={str(sn[0]):"pSheet",str(sn[1]):"pPlate",str(sn[2]):"nSheet",str(sn[3]):"nPlate"}        
        snCalc=[str(snInt)  for snInt in sn if snInt>0]
        print("snCalc:",snCalc)
        if len(snCalc)>0:
            try:
                camera = [Camera(serialNum) for serialNum in snCalc]
            except Exception as e:
                    print(str(e))
            for i in range(len(camera)):
                #camera[i].CameraOpened += Configuration.AcquireSingleFrame
                camera[i].CameraOpened += Configuration.SoftwareTrigger
        #camera.CameraOpened += Configuration.AcquireSingleFrame
        #AcquireContinuous
                camera[i].Open()
             #   camera[i].StreamGrabber.ImageGrabbed += OnImageGrabbed
                camera[i].StreamGrabber.Start()
            self.bUpdateCamClick()
    
    def capBmp(self,num,mapIndex):
        global camera
        bmpMap=["Bmp0.bmp","Bmp1.bmp","Bmp2.bmp","Bmp3.bmp"]
#        camera[num].StreamGrabber.Start()
        if camera[num].WaitForFrameTriggerReady(100, TimeoutHandling.ThrowException):
                camera[num].ExecuteSoftwareTrigger()
        grabResult = camera[num].StreamGrabber.RetrieveResult(5000, TimeoutHandling.ThrowException)
        ImagePersistence.Save(ImageFileFormat.Bmp, bmpMap[mapIndex], grabResult)
        grabResult.Dispose()
        
#        camera[num].StreamGrabber.Stop()
        
    def capEnd(self):
        global camera
        for i in range(len(camera)):
                camera[i].Close()
                camera[i].StreamGrabber.Stop()
      
#---F关闭线程功能           
    def _async_raise(self,tid, exctype):  
        """raises the exception, performs cleanup if needed"""  
        tid = c_long(tid)  
        if not inspect.isclass(exctype):  
            exctype = type(exctype)  
        res = pythonapi.PyThreadState_SetAsyncExc(tid, py_object(exctype))  
        if res == 0:  
            raise ValueError("invalid thread id")  
        elif res != 1:  
        # """if it returns a number greater than one, you're in trouble,  
        # and you should call it again with exc=NULL to revert the effect"""  
            pythonapi.PyThreadState_SetAsyncExc(tid, None)  
            raise SystemError("PyThreadState_SetAsyncExc failed")  
 
    def stop_thread(self,thread):  
        self._async_raise(thread.ident, SystemExit)  
     
#---F程序跟踪功能        
    def outDebug(self,text):
        global fd
#        fd = os.open( "debug.txt", os.O_RDWR|os.O_APPEND|os.O_CREAT )
#        # Write one string
#        line = "[ "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" ]"+text+"\n" 
#        # string needs to be converted byte object
#        b = str.encode(line)
#        os.write(fd, b)
#        # Close opened filer
#        os.close( fd)
        pass
    
#---F数据库刷新功能
    def sqlUpdate(self):
        global  cursor, p ,conn ,dictPara,basler,sn 
        cursor.execute('select * from para'  )
        value = cursor.fetchall()  
       # print(value)
        dictPara={}
        for i in range(len(value)):
            dictPara[value[i][0]]=str(value[i][1])    

#---F xml标定文件更改功能
    def xmlCalcUpdate(self,document,table,N) :         
        tree = ET.parse(document)
        root = tree.getroot() 
        nodeWorldX=[node for node in root.iter('WorldX')  ]
        nodeWorldY=[node for node in root.iter('WorldY')  ]
        nodePixelX=[node for node in root.iter('PixelX')  ]
        nodePixelY=[node for node in root.iter('PixelY')  ]    
        for i in range(0,9):
            nodeWorldX[i+N*20].text=table[0][i]
            nodeWorldY[i+N*20].text=table[1][i]
            nodePixelX[i+N*20].text=table[2][i]
            nodePixelY[i+N*20].text=table[3][i]
        tree.write(document)
#---F ACCESS数据库产量记录功能
    def accessWrite(self,JiaJuNumber,CamNumber,SaveDate,CentX,CentY,Radius,Offset,Result):
#        JiaJuNumber="0"
#        CamNumber="0"
#        SaveDate="2010"
#        CentX="0"
#        CentY="0"
#        Radius="0"
#        Offset="0"
#        Result="OK"
        rs.AddNew()
        rs.Fields.Item(1).Value = JiaJuNumber
        rs.Fields.Item(2).Value = CamNumber
        rs.Fields.Item(3).Value = SaveDate
        rs.Fields.Item(4).Value = CentX
        rs.Fields.Item(5).Value = CentY
        rs.Fields.Item(6).Value = Radius
        rs.Fields.Item(7).Value = Offset
        rs.Fields.Item(8).Value = Result
        rs.Update()
#---F图片转QPixmap功能
    def toPixImg(self,img1):
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        pixImg=QPixmap(QPixmap.fromImage(qimag1))
        return pixImg

#---F机器人OCX控件操作功能    
    def rOCXrun(self):
        global ctrMelfaRxM

        #---机器人OCX控件初始化
        ctrMelfaRxM=AxMELFARXMLib.AxMelfaRxM() 
        ((System.ComponentModel.ISupportInitialize)(ctrMelfaRxM)).BeginInit()
        form.Controls.Add(ctrMelfaRxM)
        ((System.ComponentModel.ISupportInitialize)(ctrMelfaRxM)).EndInit()
        if ctrMelfaRxM.ServerLive()==False:
            ctrMelfaRxM.ServerStart()        
    def rServer(self,robot,order):
        sSendDataON = "1" + "\n" +"1"
        sSendDataOFF = "1" + "\n" +"0"
        if order==1:
            lStatus = ctrMelfaRxM.RequestServiceM(robot, 403, len(sSendDataON), sSendDataON, 0, 0, 0)
        if order==0:
            lStatus = ctrMelfaRxM.RequestServiceM(robot, 403, len(sSendDataOFF), sSendDataOFF, 0, 0, 0)
            
    def rStop(self,robot):
        sSendData = "0"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 401, len(sSendData), sSendData, 0, 0, 0)  
    
    def rReset(self,robot):
        #错误复位
        sSendData=""
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 407, 0, sSendData, 0, 0, 0) 
        time.sleep(0.2)
        
        sSendData="1"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 409, len(sSendData), sSendData, 0, 0, 0)
        time.sleep(0.2)
        
        sSendData="2"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 409, len(sSendData), sSendData, 0, 0, 0)   
        time.sleep(0.2)
        
        sSendData=""
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 408, 0, sSendData, 0, 0, 0)  
        
        sSendData="1"+"\n"+"MAINSELECT"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 416, len(sSendData), sSendData, 0, 0, 0) 
        
        sSendData="2"+"\n"+"SELECTTHREAD"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 416, len(sSendData), sSendData, 0, 0, 0)         
    def rRunMain(self,robot):
        #修改速度
        sSendData="20"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 404, len(sSendData), sSendData, 0, 0, 0)
        time.sleep(0.5)
        sSendData="1"+"\n"+"MAINSELECT"+"\n"+"1"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 400, len(sSendData), sSendData, 0, 0, 0)         
        
    def rRunComm(self,robot):
        sSendData="2"+"\n"+"SELECTTHREAD"+"\n"+"1"
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 400, len(sSendData), sSendData, 0, 0, 0)
    
    def rWritePosition(self,robot):        
        sSendData="MAINSELECT"
        sRecvData=""
        lError=0
        self.rStop(robot)
        if robot==1:
            self.bR1run.setStyleSheet("background-color: rgb(255, 0, 0);")
        if robot==2:
            self.bR2run.setStyleSheet("background-color: rgb(255, 0, 0);")
        time.sleep(1)
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 102, len(sSendData), sSendData, 0, 0, 0)
        flag=0
        time.sleep(0.2)
        ms=ctrMelfaRxM.CheckRecvMsg()
        for i in range(ms+1): 
            if ctrMelfaRxM.CheckRecvMsg()>0:                       
                print("ctrMelfaRxM.CheckRecvMsg()",ctrMelfaRxM.CheckRecvMsg())
                a=ctrMelfaRxM.GetRecvDataM(robot,102,sRecvData,5,lError)
                print(a)
                if "MAINSELECT" in a[3]:
                    sSendData=a[3] 
                    ctrMelfaRxM.RequestServiceM(robot, 128, len(sSendData), sSendData, 0, 0, 0)
                    flag=1  
                    return 0
        lStatus = ctrMelfaRxM.RequestServiceM(robot, 102, len(sSendData), sSendData, 0, 0, 0)
        ms=ctrMelfaRxM.CheckRecvMsg()
        for i in range(ms+1): 
            if ctrMelfaRxM.CheckRecvMsg()>0:                       
                print("ctrMelfaRxM.CheckRecvMsg()",ctrMelfaRxM.CheckRecvMsg())
                a=ctrMelfaRxM.GetRecvDataM(robot,102,sRecvData,5,lError)
                print(a)
                if "MAINSELECT" in a[3]:
                    sSendData=a[3] 
                    ctrMelfaRxM.RequestServiceM(robot, 128, len(sSendData), sSendData, 0, 0, 0)
                    flag=1 
                    
                    return 0        
        b=win32api.MessageBox(0, "机器人位置数据写入失败", "机器人位置数据写入",win32con.MB_OK) 

        
        
        
        
        
        


#---F QT界面刷新程序         
    def GUIfresh(self):        
        global countPsheetOK,countPsheetNG,countNsheetOK,countNsheetNG,countPplateOK,countPplateNG,countNplateOK,countNplateNG
        global countPsheetFail,countNsheetFail,countPplateFail,countNplateFail
        global pix11,pix12,pix21,pix22
        #产量数据
        
        
        self.tPsheetTotal.setText(str(countPsheetOK+countPsheetNG))
        self.tPsheetGood.setText(str(countPsheetOK))
        self.tPsheetBad.setText(str(countPsheetNG))
        if ((countPsheetOK+countPsheetNG)>0):
            self.tPsheetGoodRate.setText(str(round(float(countPsheetOK/(countPsheetOK+countPsheetNG))*100,4)) +"%" )          
            self.tPsheetBadRate.setText(str(round(float(countPsheetNG/(countPsheetOK+countPsheetNG))*100,4))+"%"  ) 
        
        self.tPplateTotal.setText(str(countPplateOK+countPplateNG))
        self.tPplateGood.setText(str(countPplateOK))
        self.tPplateBad.setText(str(countPplateNG))
        if ((countPplateOK+countPplateNG)>0):
            self.tPplateGoodRate.setText(str(round(float(countPplateOK/(countPplateOK+countPplateNG)*100),4))+"%"  )          
            self.tPplateBadRate.setText(str(round(float(countPplateNG/(countPplateOK+countPplateNG)*100),4))+"%"  )         
        
        self.tNsheetTotal.setText(str(countNsheetOK+countNsheetNG))
        self.tNsheetGood.setText(str(countNsheetOK))
        self.tNsheetBad.setText(str(countNsheetNG))
        if ((countNsheetOK+countNsheetNG)>0):
            self.tNsheetGoodRate.setText(str(round(float(countNsheetOK/(countNsheetOK+countNsheetNG)*100),4))+"%"  )          
            self.tNsheetBadRate.setText(str(round(float(countNsheetNG/(countNsheetOK+countNsheetNG)*100),4)) +"%" )         

        self.tNplateTotal.setText(str(countNplateOK+countNplateNG))
        self.tNplateGood.setText(str(countNplateOK))
        self.tNplateBad.setText(str(countNplateNG))
        if ((countNplateOK+countNplateNG)>0):
            self.tNplateGoodRate.setText(str(round(float(countNplateOK/(countNplateOK+countNplateNG)*100),4))+"%" )          
            self.tNplateBadRate.setText(str(round(float(countNplateNG/(countNplateOK+countNplateNG)*100),4)) +"%" )                                           
        
        self.tPsheetFail.setText(str(countPsheetFail))
        self.tPplateFail.setText(str(countPplateFail))        
        self.tNsheetFail.setText(str(countNsheetFail))       
        self.tNplateFail.setText(str(countNplateFail))
        
        self.tPsheetPixMM.setText(str(pix11))
        self.tPplatePixMM.setText(str(pix12))        
        self.tNsheetPixMM.setText(str(pix21))       
        self.tNplatePixMM.setText(str(pix22))        
                        
        self.bDataSaveClick()
        
        
        
        
#MAINSELECT
#---F QT界面刷新线程             
class MyThread(QThread):
    sinOut = pyqtSignal(str)   
    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)
        self.identity = None        
    def setIdentity(self,text):
        self.identity = text
    def setVal(self,val):
        self.times = int(val)
        # 执行线程的run方法
        self.start()        
    def run(self):
        while self.times > 0 and self.identity:
            # 发射信号
            self.sinOut.emit(self.identity+"==>"+str(self.times))
            time.sleep(2)
            


##子窗口
#qtCreatorFile = "visionPara.ui" # Enter file here.导入文件
#Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
#class Vison(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
##    close_signal = pyqtSignal()
#    def __init__(self):
#        global  cursor,paraName, paraData ,conn,dictParaVision                              #初始化
#        QtWidgets.QMainWindow.__init__(self)
#        Ui_MainWindow.__init__(self)        
#        self.setupUi(self)
#        self.bSaveData.clicked.connect(self.bSaveDataClick)
#        self.sqlUpdate()
#        
#        self.pSheetT1.setText(dictParaVision['pSheetT1'])
#        self.pSheetT2.setText(dictParaVision['pSheetT2'])
#        self.pSheetCmin.setText(dictParaVision['pSheetCmin'])
#        self.pSheetCmax.setText(dictParaVision['pSheetCmax'])
#        self.pSheetSmin.setText(dictParaVision['pSheetSmin'])
#        self.pSheetSmax.setText(dictParaVision['pSheetSmax'])
#        
#        self.nSheetT1.setText(dictParaVision['nSheetT1'])
#        self.nSheetT2.setText(dictParaVision['nSheetT2'])
#        self.nSheetCmin.setText(dictParaVision['nSheetCmin'])
#        self.nSheetCmax.setText(dictParaVision['nSheetCmax'])
#        self.nSheetSmin.setText(dictParaVision['nSheetSmin'])
#        self.nSheetSmax.setText(dictParaVision['nSheetSmax'])
#        
#        self.pPlateT1.setText(dictParaVision['pPlateT1'])
#        self.pPlateT2.setText(dictParaVision['pPlateT2'])
#        self.pPlateCmin.setText(dictParaVision['pPlateCmin'])
#        self.pPlateCmax.setText(dictParaVision['pPlateCmax'])
#        self.pPlateSmin.setText(dictParaVision['pPlateSmin'])        
#        self.pPlateSmax.setText(dictParaVision['pPlateSmax']) 
#
#        self.nPlateT1.setText(dictParaVision['nPlateT1'])
#        self.nPlateT2.setText(dictParaVision['nPlateT2'])
#        self.nPlateCmin.setText(dictParaVision['nPlateCmin'])
#        self.nPlateCmax.setText(dictParaVision['nPlateCmax'])
#        self.nPlateSmin.setText(dictParaVision['nPlateSmin'])        
#        self.nPlateSmax.setText(dictParaVision['nPlateSmax'])   
#    def sqlUpdate(self):
#        global  cursor,paraName, paraData ,conn,dictParaVision 
#        cursor.execute('select * from paraVision'  )
#        value = cursor.fetchall()   
#        dictParaVision={}
#        for i in range(len(value)):
#            dictParaVision[value[i][0]]=str(value[i][1])
#        print(dictParaVision)
#    def bSaveDataClick(self):  
#        global dictParaVision
#        dictParaVision['pSheetT1']=self.pSheetT1.toPlainText()
#        dictParaVision['pSheetT2']=self.pSheetT2.toPlainText()
#        dictParaVision['pSheetCmin']=self.pSheetCmin.toPlainText()                 
#        dictParaVision['pSheetCmax']=self.pSheetCmax.toPlainText() 
#        dictParaVision['pSheetSmin']=self.pSheetSmin.toPlainText()                 
#        dictParaVision['pSheetSmax']=self.pSheetSmax.toPlainText()         
#
#        dictParaVision['nSheetT1']=self.nSheetT1.toPlainText()
#        dictParaVision['nSheetT2']=self.nSheetT2.toPlainText()
#        dictParaVision['nSheetCmin']=self.nSheetCmin.toPlainText()                 
#        dictParaVision['nSheetCmax']=self.nSheetCmax.toPlainText() 
#        dictParaVision['nSheetSmin']=self.nSheetSmin.toPlainText()                 
#        dictParaVision['nSheetSmax']=self.nSheetSmax.toPlainText()          
#        
#        dictParaVision['pPlateT1']=self.pPlateT1.toPlainText()
#        dictParaVision['pPlateT2']=self.pPlateT2.toPlainText()
#        dictParaVision['pPlateCmin']=self.pPlateCmin.toPlainText()                 
#        dictParaVision['pPlateCmax']=self.pPlateCmax.toPlainText() 
#        dictParaVision['pPlateSmin']=self.pPlateSmin.toPlainText()                 
#        dictParaVision['pPlateSmax']=self.pPlateSmax.toPlainText()         
#
#        dictParaVision['nPlateT1']=self.nPlateT1.toPlainText()
#        dictParaVision['nPlateT2']=self.nPlateT2.toPlainText()
#        dictParaVision['nPlateCmin']=self.nPlateCmin.toPlainText()                 
#        dictParaVision['nPlateCmax']=self.nPlateCmax.toPlainText() 
#        dictParaVision['nPlateSmin']=self.nPlateSmin.toPlainText()                 
#        dictParaVision['nPlateSmax']=self.nPlateSmax.toPlainText()           
#       # print(dictPara)
#        for key in dictParaVision:
#            cursor.execute("update paraVision set data=? where name = ?",(dictParaVision[key],key,))        
#        conn.commit()        
#        self.outDebug("保存系统参数")
#    def handle_click(self):
##        if not self.isVisible():
#        self.show()    
#def windowConn():    
#    mainWindow.bVisionPara.clicked.connect(visionWindow.handle_click)
#    visionWindow.bPsheetTrig.clicked.connect(mainWindow.bPsheetTrigClick)  
#    visionWindow.bPplateTrig.clicked.connect(mainWindow.bPplateTrigClick) 
#    visionWindow.bNsheetTrig.clicked.connect(mainWindow.bNsheetTrigClick) 
#    visionWindow.bNplateTrig.clicked.connect(mainWindow.bNplateTrigClick) 
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApp()
 #   visionWindow=Vison()
  #  windowConn()
#    mainWindow.show()
    app.setActiveWindow(mainWindow)
    mainWindow.showMaximized() 
#    mainWindow.showFullScreen() 
    sys.exit(app.exec_())

