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

import threading
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
#import cv2
import numpy as np
import win32api,win32con  
import os, sys
import System
import System.Drawing
import socketClient
#import time
#from PyQt5 import *
#import datetime
import time
qtCreatorFile = "window.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
    global flag
#---初始化
    def __init__(self):
        global  cursor,conn ,dictPara ,flag,bf,rf,gf,yf              #初始化
        global sockPs,sockPr,sockNs,sockNr
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        #---加载sqlite3参数数据库，程序所有参数
        conn = sqlite3.connect("3d.db")
        cursor = conn.cursor()
        self.sqlUpdate()
   
        #---主界面按钮
        #数据复位，保存 ，操作面板     
        self.bDataReset.clicked.connect(self.bDataResetClick)
        self.bDataSave.clicked.connect(self.bDataSaveClick)     
        self.bAuto.clicked.connect(self.bAutoClick) 
        self.bReset.clicked.connect(self.bResetClick) 
        self.bStop.clicked.connect(self.bStopClick)    
        
        self.bRed.clicked.connect(self.bRedClick)     
        self.bGreen.clicked.connect(self.bGreenClick) 
        self.bYellow.clicked.connect(self.bYellowClick) 
        self.bBuzz.clicked.connect(self.bBuzzClick)                
                        
        #---检测设定界面按钮
        #浏览
        self.bSelectDoc.clicked.connect(self.bSelectDocClick)
        
        #---视觉调试界面按钮                                
      
        #实时，触发
        
        self.bLUtrig.clicked.connect(self.bLUtrigClick)  
        self.bLDtrig.clicked.connect(self.bLDtrigClick) 
        self.bRUtrig.clicked.connect(self.bRUtrigClick) 
        self.bRDtrig.clicked.connect(self.bRDtrigClick)
        self.bC1trig.clicked.connect(self.bC1trigClick) 
        self.bC2trig.clicked.connect(self.bC2trigClick)        
        self.bCyUp.clicked.connect(self.bCyUpClick)
        self.bCyDown.clicked.connect(self.bCyDownClick)
        self.bLposition0.clicked.connect(self.bLposition0Click)
        self.bLposition1.clicked.connect(self.bLposition1Click)
        self.bLposition2.clicked.connect(self.bLposition2Click)        
        self.bRposition0.clicked.connect(self.bRposition0Click)
        self.bRposition1.clicked.connect(self.bRposition1Click)
        self.bRposition2.clicked.connect(self.bRposition2Click)        
        self.bAxiSave.clicked.connect(self.bAxiSaveClick)        
       
                
               
        #---历史数据界面按钮
   
        self.bExport.clicked.connect(self.bExportClick)
       
        
        #---QT界面数据刷新线程                
        self.thread = MyThread()
        self.thread.setIdentity("thread1")
        self.thread.sinOut.connect(self.GUIfresh)
        self.thread.setVal(2)        
                
#        fd = os.open( "debug.txt", os.O_RDWR|os.O_APPEND )                   
        #---QT界面初始化        
        #标定控件隐藏效果
#        self.bPsheetToolCalcNext.hide()
#        self.bPplateToolCalcNext.hide()
#        self.bNsheetToolCalcNext.hide()
#        self.bNplateToolCalcNext.hide()
#        self.tR1Mspeed.setText("10")
#        self.tR2Mspeed.setText("10")
#        #视学调试，表格标题
#        self.tableWidgetPs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
#        self.tableWidgetPp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
#        self.tableWidgetNs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y'])  
#        self.tableWidgetNp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
        #产量数据
        self.tTime.setText(dictPara['tTime'])
        self.tTotal.setText(dictPara['tTotal'])
        self.tGood.setText(dictPara['tGood'])
        self.tGoodRate.setText(dictPara['tGoodRate'])
        self.tBad.setText(dictPara['tBad'])
        self.tBadRate.setText(dictPara['tBadRate'])
        self.tFail.setText(dictPara['tFail'])

        #机器人IP参数       
        self.tLUip.setText(dictPara['tLUip'])
        self.tLDip.setText(dictPara['tLDip'])
        self.tRUip.setText(dictPara['tRUip'])
        self.tRDip.setText(dictPara['tRDip'])  
        self.tC1ip.setText(dictPara['tC1ip'])
        self.tC2ip.setText(dictPara['tC2ip'])          
        # 轴参数设置
        self.tSpeed.setText(dictPara['tSpeed'])
        self.tPosion1.setText(dictPara['tPosion1'])
        self.tPosion2.setText(dictPara['tPosion2'])   
        try:
            import PLC
            PLC.write("101",hex(int(dictPara['tSpeed']))[2:len(hex(int(dictPara['tSpeed'])))])
            PLC.write("102",hex(int(dictPara['tPosion1']))[2:len(hex(int(dictPara['tPosion1'])))])
            PLC.write("103",hex(int(dictPara['tPosion2']))[2:len(hex(int(dictPara['tPosion2'])))])
        except Exception as e:
            print(str(e))
            
        
        #视觉判定参数
        #   正极过渡片
        self.tStandardH.setText(dictPara['tStandardH'])
        self.tStandardD.setText(dictPara['tStandardD'])
        self.tNGpath.setText(dictPara['tNGpath'])
        
      
        
        #---全局变量初始化
        flag=0
        rf=0
        gf=0
        yf=0
        bf=0
        #---启动子程序
        try:
            sockPs=socketClient.connect(dictPara['tC1ip'],2003)
            sockPr=socketClient.connect(dictPara['tC1ip'],2004)
        
            sockNs=socketClient.connect(dictPara['tC2ip'],2005)
            sockNr=socketClient.connect(dictPara['tC2ip'],2006)   
        except Exception as e:
            print(str(e))            

#        PLC.openSerial()


#---事件     
    def closeEvent(self, event):
        global ctrMelfaRxM
        try:
            pass
        except:
            pass
        self.close()
        os._exit(0)
        
#---主界面按钮事件 
    #---自动运行
    def bAutoClick(self):  
       
        pass

    #---暂停    
    def bStopClick(self):  
        pass
    #---复位
    def bResetClick(self):  
#        PLC.on("100",8)
#        time.sleep(0.1)
#        PLC.off("100",8)
        pass 
    #---红灯
    def bRedClick(self): 
        global flag,rf
        
        flag=1
        if rf==0:
            PLC.on("100",9)
            rf=1
            flag=0
            return 0
        if rf==1:
            PLC.off("100",9) 
            rf=0
        flag=0
        pass  
 
    #---绿灯
    def bGreenClick(self):  
        global flag,gf
        flag=1
        
        if gf==0:
            PLC.on("100",10)
            gf=1
            flag=0
            return 0
        time.sleep(0.1)
        if gf==1:
            PLC.off("100",10) 
            gf==0
        flag=0
        pass          
        pass     
    #---黄灯
    def bYellowClick(self): 
        global flag,yf
        flag=1
        if yf==0:
            PLC.on("100",11)
            yf=1
            flag=0
            return 0
        if yf==1:
            

            PLC.off("100",11) 
            yf=0
        flag=0
        pass          
        pass    
    #---蜂鸣器
    def bBuzzClick(self):
        global flag,bf
        flag=1
        if bf==0:
            PLC.on("100",12)
            bf=1
            flag=0
            return 0
        if bf==1:
            PLC.off("100",12) 
            bf=0
        flag=0
        pass          
        pass      
        
    #---重置数据
    def bDataResetClick(self): 
        global countPsheetFail,countNsheetFail,countPplateFail,countNplateFail
        global countPsheetOK,countPsheetNG,countNsheetOK,countNsheetNG,countPplateOK,countPplateNG,countNplateOK,countNplateNG
        currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.tTime.setText(currentTime)
        
        self.tTotal.setText('0')
        self.tGood.setText('0')
        self.tGoodRate.setText('0')
        self.tBad.setText('0')
        self.tBadRate.setText('0')
        self.tFail.setText('0')
 
        self.outDebug("统计信息重置")  
    #---保存数据
    def bDataSaveClick(self): 
        global paraName, conn,cursor,dictPara
        dictPara['tTime']=self.tTime.toPlainText()
        dictPara['tTotal']=self.tTotal.toPlainText()
        dictPara['tGood']=self.tGood.toPlainText()
        dictPara['tGoodRate']=self.tGoodRate.toPlainText()
        dictPara['tBad']=self.tBad.toPlainText()
        dictPara['tBadRate']=self.tBadRate.toPlainText()
        dictPara['tFail']=self.tFail.toPlainText()
        
        dictPara['tLUip']=self.tLUip.toPlainText()
        dictPara['tLDip']=self.tLDip.toPlainText()        
        dictPara['tRUip']=self.tRUip.toPlainText()        
        dictPara['tRDip']=self.tRDip.toPlainText()
        dictPara['tC1ip']=self.tC1ip.toPlainText()
        dictPara['tC2ip']=self.tC2ip.toPlainText()
        
        dictPara['tSpeed']=self.tSpeed.toPlainText()
        dictPara['tPosion1']=self.tPosion1.toPlainText()
        dictPara['tPosion2']=self.tPosion2.toPlainText()
        
        dictPara['tStandardH']=self.tStandardH.toPlainText()
        dictPara['tStandardD']=self.tStandardD.toPlainText()
        dictPara['tNGpath']=self.tNGpath.toPlainText()
                        
       # print(dictPara)
        for key in dictPara:
            cursor.execute("update para set data=? where name = ?",(dictPara[key],key,))        
        conn.commit()
        self.outDebug("系统参数保存")
       # b=win32api.MessageBox(0, "保存成功", "参数保存",win32con.MB_OK)
        
         
            
            
            
#---检测设定界面，按钮事件    
    def bSelectDocClick(self):  
        directory1 = QFileDialog.getExistingDirectory(self,  "选取文件夹",  "D:/") #起始路径  
        self.tNGpath.setText(directory1) 
        self.outDebug("修改NG文件夹:"+directory1)
#        print(directory1)
#        img1=cv2.imread("arrayBmp0.bmp")
#        cv2.imwrite(directory1+"/arrayBmp3.bmp",img1) 

 
#---视觉调试界面，按钮事件    
    #---相机触发

    #bTrigFunc相机触发功能函数
    def bTrigFunc(self,sn,file,camNum,camName,visionStand):
        pass
            
    def bLUtrigClick(self):
        pass
            
    def bLDtrigClick(self):
        pass
    
    def bRUtrigClick(self):
        pass
    
    def bRDtrigClick(self):
        pass  
    
    def bC1trigClick(self):
        global sockPs,sockPr,sockNs,sockNr
        socketClient.sent(sockPs,"TRG")
        msg=socketClient.rev(sockPr,1024)   
        print("msg:",msg)
        self.tCode1.setText(str(msg))

        pass      
    
    def bC2trigClick(self):
        global sockPs,sockPr,sockNs,sockNr
        socketClient.sent(sockNs,"TRG")
        msg=socketClient.rev(sockNr,1024)   
        print("msg:",msg)
        self.tCode2.setText(str(msg))        
        pass   
 
    #---机台手动按钮
    
    def bCyUpClick(self):
        global flag
        flag=1
        PLC.on("100",6)
        time.sleep(0.1)
        PLC.off("100",7) 
        flag=0
        pass          
    
    def bCyDownClick(self):
        global flag
        flag=1
        PLC.on("100",7)
        time.sleep(0.1)
        PLC.off("100",6)       
        flag=0
        pass      
    
    def bLposition0Click(self):
        global flag
        flag=1
        PLC.on("100",0)
        time.sleep(0.1)
        PLC.off("100",0)
        flag=0
        pass   
    
    def bLposition1Click(self):
        global flag
        flag=1
        PLC.on("100",1)
        time.sleep(0.1)
        PLC.off("100",1)
        flag=0
        pass     
    def bLposition2Click(self):
        global flag
        flag=1
        PLC.on("100",2)
        time.sleep(0.1)
        PLC.off("100",2)     
        flag=0
        pass  
     
    def bRposition0Click(self):
        global flag
        flag=1
        PLC.on("100",3)
        time.sleep(0.1)
        PLC.off("100",3)   
        flag=0
        pass   
    
    def bRposition1Click(self):
        global flag
        flag=1
        PLC.on("100",4)
        time.sleep(0.1)
        PLC.off("100",4)      
        flag=0
        pass     
    def bRposition2Click(self):
        global flag
        flag=1
        PLC.on("100",5)
        time.sleep(0.1)
        PLC.off("100",5)
        flag=0
        pass   

#---历史数据界面，按钮事件    
    def bExportClick(self):
        pass    
    
#---写入PLC数据界面，按钮事件    
    def bAxiSaveClick(self):
        PLC.write("101",hex(int(dictPara['tSpeed']))[2:len(hex(int(dictPara['tSpeed'])))])
        PLC.write("102",hex(int(dictPara['tPosion1']))[2:len(hex(int(dictPara['tPosion1'])))])
        PLC.write("103",hex(int(dictPara['tPosion2']))[2:len(hex(int(dictPara['tPosion2'])))])
        pass  

      
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

#---F图片转换
    def toPixImg(self,img1):
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        pixImg=QPixmap(QPixmap.fromImage(qimag1))
        return pixImg
                          
#---F QT界面刷新程序         
    def GUIfresh(self):  
        global flag
        con=[self.bLposition0,self.bLposition1,self.bLposition2,\
             self.bRposition0,self.bRposition1,self.bRposition2,\
             self.bCyUp,self.bCyDown,self.bRed,self.bGreen,self.bYellow,self.bBuzz]
        if flag==0:            
            state=PLC.readState()
            for i in range(len(con)):
                if state[i]== True:
                    con[i].setStyleSheet("background-color: rgb(0, 255, 0);")
                else:
                    con[i].setStyleSheet("background-color: rgb(255, 0, 0);")
     
            
                      
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
            time.sleep(1)
            

  
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

