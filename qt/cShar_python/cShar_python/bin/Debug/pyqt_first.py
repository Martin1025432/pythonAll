from __future__ import division
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QThread ,  pyqtSignal

import time
import sqlite3
import pandas
import collections  
import cv2
import dll
from ctypes import * 
import threading
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
#import cv2
import numpy as np
#import time
#from PyQt5 import *
import datetime
qtCreatorFile = "window.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
    def __init__(self):
        global  cursor, p ,conn ,dictPara,basler,sn                      #初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        self.bDataReset.clicked.connect(self.bDataResetClick)
        self.bDataSave.clicked.connect(self.bDataSaveClick)
        self.bRun.clicked.connect(self.bRunClick)
        self.bTCPini.clicked.connect(self.bTCPiniClick)
        self.bPsent.clicked.connect(self.bPsentClick)
        self.bNsent.clicked.connect(self.bNsentClick)
        self.thread = MyThread()
        self.thread.setIdentity("thread1")
        self.thread.sinOut.connect(self.outText)
        self.thread.setVal(100)        
        
               
        conn = sqlite3.connect("cm08.db")
        cursor = conn.cursor()
        self.sqlUpdate()
#        cursor.execute('select * from para'  )
#
#        value = cursor.fetchall()  
#        print(value)
#        dictPara={}
#        for i in range(len(value)):
#            dictPara[value[i][0]]=str(value[i][1])
#        print(dictPara)
        
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
        #系统设定        
        self.tPip.setText(dictPara['tPip'])
        self.tNip.setText(dictPara['tNip'])
        self.tTCPport.setText(dictPara['tTCPport'])
        self.tIP.setText(dictPara['tIP'])
        #初始化相机
        sn=[]
        basler=CDLL('vision.dll')
        try:
            basler.capIni()
            for i in range(0,4):  
                sizebuffer=basler.outputStr(i)
                print(c_char_p(sizebuffer).value)
                recStr=str(c_char_p(sizebuffer).value)[2:-1]
                sn.append(recStr)
        except:
            self.info.setText("相机打开失败")
    global     nData    
    def sqlUpdate(self):
        global  cursor, p ,conn ,dictPara,basler,sn 
        cursor.execute('select * from para'  )
        value = cursor.fetchall()  
        print(value)
        dictPara={}
        for i in range(len(value)):
            dictPara[value[i][0]]=str(value[i][1])
    def outText(self):
        global nData,pData,nSoc,pSoc,cent 
        
        try:
            if(pData==b'TRGS'):
#                self.tPrec.setText(str(pData))
                self.bPsheetTrigClick()

                pSoc.send(bytes(str(cent),'utf8'))
        except:
            pass
        pData=b''
    def server(self,serverAddr,nClientIP,pClientIP):
        global nData,pData,nSoc,pSoc 
        mulLock = threading.Lock()  
        serverSoc = socket(AF_INET, SOCK_STREAM)
        serverSoc.bind(serverAddr)
        serverSoc.listen(5)
        while True:
    # 接受一个新连接:
            sock, addr = serverSoc.accept()
            if(addr[0]==nClientIP):
    # 创建新线程来处理TCP连接:
                print(sock)
                nData='conned'
                nSoc=sock            
                t = threading.Thread(target=self.tcplink, args=(sock, addr,nClientIP,pClientIP))
                t.start()
                print('nclien',nData)
            if(addr[0]==pClientIP):
    # 创建新线程来处理TCP连接:
                print(addr)
                pData='conned'
                pSoc=sock   
                try:                
                    t = threading.Thread(target=self.tcplink, args=(sock, addr,nClientIP,pClientIP))
                    t.start()
                    print('pclien',pData)
                except:
                    print('error')
    def tcplink(self,sock, addr,nClientIP,pClientIP):
        global nData,pData,nSoc,pSoc,centPsheet, centNsheet,centPplate, centNplate
        while True:
            try:
                data = sock.recv(1024)
                if(data!=''):
                    if(addr[0]==nClientIP):
                        nData=data
                        print(nData)
                        self.tNrec.setText(str(nData))
                        if(nData==b'TRGS'):

                            self.bNsheetTrigClick()
                            try:
                                nSoc.send(bytes(str(centNsheet),'utf8'))
                            except:
                                print("erro find")    
                            nData=b''
                        if(nData==b'TRGP'):

                            self.bNplateTrigClick()
                            try:
                                nSoc.send(bytes(str(centNplate),'utf8'))
                            except:
                                print("erro find")    
                            nData=b''                                                                                                                             
                    if(addr[0]==pClientIP):
                        pData=data 
                        print(pData)
                        self.tPrec.setText(str(pData))
                        if(pData==b'TRGS'):

                            self.bPsheetTrigClick()
                            try:
                                pSoc.send(bytes(str(centPsheet),'utf8'))
                            except:
                                print("erro find")    
                            pData=b''
                        if(pData==b'TRGP'):

                            self.bPplateTrigClick()
                            try:
                                pSoc.send(bytes(str(centPplate),'utf8'))
                            except:
                                print("erro find")    
                            pData=b''                                  
                if data == 'exit' or not data:
                    break
            except:
                print('error')
        sock.close()
        print ('Connection from closed.')     
    def bTCPiniClick(self):
        addr=(dictPara['tIP'],int(dictPara['tTCPport']))
        print(addr)
        sv = threading.Thread(target=self.server, args=(addr,dictPara['tNip'],dictPara['tPip']))

        sv.start()        
    
    def bDataResetClick(self): 
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
        
       # print(dictPara)
        for key in dictPara:
            cursor.execute("update para set data=? where name = ?",(dictPara[key],key,))        
        conn.commit()
        
    def bRunClick(self): 
        global basler,dictPara,basler,sn,basler,dictPara,pData,pData
        self.bTCPiniClick()
#        while(1):
#            time.sleep(1)
#            
#            try:
#
#                if(pData!=""):
#                    self.bPsheetTrigClick()
#                    pData=""
#            except:
#                pass



                 
    def bPsheetTrigClick(self):
        global basler,sn,dictPara,dictParaVision,centPsheet       
        print("P sheet camer trig ")
        print(datetime.datetime.now())
        basler.capBmp(sn.index(dictPara['tPsheetSn']))
        print(datetime.datetime.now())
        img1=cv2.imread('bmpForProcess.bmp')
        print(datetime.datetime.now())
        img1Processed=img1.copy()                        
        try:
            print(datetime.datetime.now())
            cent=dll.findEdge(int(dictParaVision['pSheetT1']),int(dictParaVision['pSheetT2']),img1,img1Processed,int(dictParaVision['pSheetCmin']),int(dictParaVision['pSheetCmax']),int(dictParaVision['pSheetSmin']),int(dictParaVision['pSheetSmax']))
            img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
            qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
            self.lCamSheetP.setPixmap(QPixmap(QPixmap.fromImage(qimag1)))
            print(datetime.datetime.now())

        except:
            self.lCamSheetP.setText('error')
    def bPplateTrigClick(self):
        global basler,sn,dictPara,dictParaVision,centPplate
        print("P plate camer trig ")
        s1=time.time()
        basler.capBmp(sn.index(dictPara['tPplateSn']))
        try:
            #basler.capBmp(sn.index(dictPara['tPplateSn']))
            e1=time.time()
            capTime="Cap time:"+str(round((e1-s1),2))
            
            
            img1=cv2.imread('bmpForProcess.bmp')        
        
            img1Processed=img1.copy()
            centPplate=dll.findEdge(int(dictParaVision['pPlateT1']),int(dictParaVision['pPlateT2']),img1,img1Processed,int(dictParaVision['pPlateCmin']),int(dictParaVision['pPlateCmax']),int(dictParaVision['pPlateSmin']),int(dictParaVision['pPlateSmax']))
            e2=time.time()
            processTime="Process time:"+str(round((e2-e1),2))

            cv2.putText(img1,capTime,(10,400),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            cv2.putText(img1,processTime,(10,500),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
            qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
            self.lCamPlateP.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
            
        except:
            self.lCamPlateP.setText('error')
    def bNsheetTrigClick(self):
        global basler,sn,dictPara,dictParaVision,centNsheet
        print("N sheet camer trig ")
        s1=time.time()
      #  basler.capBmp(sn.index(dictPara['tNsheetSn']))
        try:
            #basler.capBmp(sn.index(dictPara['tPplateSn']))
            e1=time.time()
            capTime="Cap time:"+str(round((e1-s1),2))
            
            
            img1=cv2.imread('bmpForProcess.bmp')        
        
            img1Processed=img1.copy()
            centNsheet=dll.findEdge(int(dictParaVision['nSheetT1']),int(dictParaVision['nSheetT2']),img1,img1Processed,int(dictParaVision['nSheetCmin']),int(dictParaVision['nSheetCmax']),int(dictParaVision['nSheetSmin']),int(dictParaVision['nSheetSmax']))
            e2=time.time()
            processTime="Process time:"+str(round((e2-e1),2))

            cv2.putText(img1,capTime,(10,400),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            cv2.putText(img1,processTime,(10,500),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
            qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
            self.lCamSheetN.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
            
        except:
            self.lCamPlateP.setText('error')
    def bNplateTrigClick(self):
        global basler,sn,dictPara,dictParaVision,centNplate
        print("N plate camer trig ")
        try:
            basler.capBmp(sn.index(dictPara['tNplateSn']))
            img1=cv2.imread('bmpForProcess.bmp')              
            img1Processed=img1.copy()
            centNplate=dll.findEdge(int(dictParaVision['bPsheetT1']),int(dictParaVision['bPsheetT2']),img1,img1Processed,int(dictParaVision['pSheetCmin']),int(dictParaVision['pSheetCmax']),int(dictParaVision['pSheetSmin']),int(dictParaVision['pSheetSmax']))
            img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
            qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
            self.lCamPlateN.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
        except:
            self.lCamPlateN.setText('error')
                 
    def bPsentClick(self):
        global basler,dictPara,pData,pSoc
        pSoc.send(bytes(self.tPsent.toPlainText(),'utf8'))
    
                        
    def bNsentClick(self):
        global basler,dictPara,nData,nSoc
        nSoc.send(bytes(self.tNsent.toPlainText(),'utf8'))
        


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
#        self.start()        
    def run(self):
        while self.times > 0 and self.identity:
            # 发射信号
            self.sinOut.emit(self.identity+"==>"+str(self.times))
            time.sleep(1)
#            self.times -= 1


#子窗口
qtCreatorFile = "visionPara.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class Vison(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
#    close_signal = pyqtSignal()
    def __init__(self):
        global  cursor,paraName, paraData ,conn,dictParaVision                              #初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        self.bSaveData.clicked.connect(self.bSaveDataClick)
        self.sqlUpdate()
        
        self.pSheetT1.setText(dictParaVision['pSheetT1'])
        self.pSheetT2.setText(dictParaVision['pSheetT2'])
        self.pSheetCmin.setText(dictParaVision['pSheetCmin'])
        self.pSheetCmax.setText(dictParaVision['pSheetCmax'])
        self.pSheetSmin.setText(dictParaVision['pSheetSmin'])
        self.pSheetSmax.setText(dictParaVision['pSheetSmax'])
        
        self.nSheetT1.setText(dictParaVision['nSheetT1'])
        self.nSheetT2.setText(dictParaVision['nSheetT2'])
        self.nSheetCmin.setText(dictParaVision['nSheetCmin'])
        self.nSheetCmax.setText(dictParaVision['nSheetCmax'])
        self.nSheetSmin.setText(dictParaVision['nSheetSmin'])
        self.nSheetSmax.setText(dictParaVision['nSheetSmax'])
        
        self.pPlateT1.setText(dictParaVision['pPlateT1'])
        self.pPlateT2.setText(dictParaVision['pPlateT2'])
        self.pPlateCmin.setText(dictParaVision['pPlateCmin'])
        self.pPlateCmax.setText(dictParaVision['pPlateCmax'])
        self.pPlateSmin.setText(dictParaVision['pPlateSmin'])        
        self.pPlateSmax.setText(dictParaVision['pPlateSmax']) 

        self.nPlateT1.setText(dictParaVision['nPlateT1'])
        self.nPlateT2.setText(dictParaVision['nPlateT2'])
        self.nPlateCmin.setText(dictParaVision['nPlateCmin'])
        self.nPlateCmax.setText(dictParaVision['nPlateCmax'])
        self.nPlateSmin.setText(dictParaVision['nPlateSmin'])        
        self.nPlateSmax.setText(dictParaVision['nPlateSmax'])   
    def sqlUpdate(self):
        global  cursor,paraName, paraData ,conn,dictParaVision 
        cursor.execute('select * from paraVision'  )
        value = cursor.fetchall()   
        dictParaVision={}
        for i in range(len(value)):
            dictParaVision[value[i][0]]=str(value[i][1])
        print(dictParaVision)
    def bSaveDataClick(self):  
        global dictParaVision
        dictParaVision['pSheetT1']=self.pSheetT1.toPlainText()
        dictParaVision['pSheetT2']=self.pSheetT2.toPlainText()
        dictParaVision['pSheetCmin']=self.pSheetCmin.toPlainText()                 
        dictParaVision['pSheetCmax']=self.pSheetCmax.toPlainText() 
        dictParaVision['pSheetSmin']=self.pSheetSmin.toPlainText()                 
        dictParaVision['pSheetSmax']=self.pSheetSmax.toPlainText()         

        dictParaVision['nSheetT1']=self.nSheetT1.toPlainText()
        dictParaVision['nSheetT2']=self.nSheetT2.toPlainText()
        dictParaVision['nSheetCmin']=self.nSheetCmin.toPlainText()                 
        dictParaVision['nSheetCmax']=self.nSheetCmax.toPlainText() 
        dictParaVision['nSheetSmin']=self.nSheetSmin.toPlainText()                 
        dictParaVision['nSheetSmax']=self.nSheetSmax.toPlainText()          
        
        dictParaVision['pPlateT1']=self.pPlateT1.toPlainText()
        dictParaVision['pPlateT2']=self.pPlateT2.toPlainText()
        dictParaVision['pPlateCmin']=self.pPlateCmin.toPlainText()                 
        dictParaVision['pPlateCmax']=self.pPlateCmax.toPlainText() 
        dictParaVision['pPlateSmin']=self.pPlateSmin.toPlainText()                 
        dictParaVision['pPlateSmax']=self.pPlateSmax.toPlainText()         

        dictParaVision['nPlateT1']=self.nPlateT1.toPlainText()
        dictParaVision['nPlateT2']=self.nPlateT2.toPlainText()
        dictParaVision['nPlateCmin']=self.nPlateCmin.toPlainText()                 
        dictParaVision['nPlateCmax']=self.nPlateCmax.toPlainText() 
        dictParaVision['nPlateSmin']=self.nPlateSmin.toPlainText()                 
        dictParaVision['nPlateSmax']=self.nPlateSmax.toPlainText()           
       # print(dictPara)
        for key in dictParaVision:
            cursor.execute("update paraVision set data=? where name = ?",(dictParaVision[key],key,))        
        conn.commit()        
        
    def handle_click(self):
#        if not self.isVisible():
        self.show()    
def windowConn():    
    mainWindow.bVisionPara.clicked.connect(visionWindow.handle_click)
    visionWindow.bPsheetTrig.clicked.connect(mainWindow.bPsheetTrigClick)  
    visionWindow.bPplateTrig.clicked.connect(mainWindow.bPplateTrigClick) 
    visionWindow.bNsheetTrig.clicked.connect(mainWindow.bNsheetTrigClick) 
    visionWindow.bNplateTrig.clicked.connect(mainWindow.bNplateTrigClick) 
#if __name__ == "__main__":
#    cap = cv2.VideoCapture(0)
#    cap.set(3,2592)   
#    cap.set(4,1944)      
app = QtWidgets.QApplication(sys.argv)
mainWindow = MyApp()
visionWindow=Vison()
windowConn()
mainWindow.show()
sys.exit(app.exec_())
