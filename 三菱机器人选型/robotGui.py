from __future__ import division

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage,QStandardItem
from PyQt5.QtCore import QThread ,  pyqtSignal
from PyQt5.QtWidgets import QFileDialog ,QTableWidgetItem
import time
import inspect 
import sqlite3
import pandas
import collections  

import math

import threading

#import cv2
import numpy as np
import win32api,win32con  
import os, sys


#import time
#from PyQt5 import *
#import datetime

qtCreatorFile = "robot.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类

#---初始化
    def __init__(self):
        global  cursor,conn ,dictPara               #初始化

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        #---加载sqlite3参数数据库，程序所有参数
        conn = sqlite3.connect("robot.db")
        cursor = conn.cursor()

   
        #---主界面按钮
        #数据复位，保存 ，操作面板     
        tool=[self.bChoose,self.bCalc,self.tResult,self.bCalc2]
        func=[self.bChooseClick,self.bCalcClick,self.bUpdateClick,self.bCalc2Click]
#        self.bChoose.clicked.connect(self.bChooseClick)
#        self.bCalc.clicked.connect(self.bCalcClick)     
#        self.tResult.clicked.connect(self.bUpdateClick)      
#        self.bCalc2.clicked.connect(self.bCalc2Click)     
        for i in range(len(tool)) :
            tool[i].clicked.connect(func[i])
        
  

#        #视学调试，表格标题
#        self.tableWidgetPs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
#        self.tableWidgetPp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
#        self.tableWidgetNs.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y'])  
#        self.tableWidgetNp.setHorizontalHeaderLabels(['机器人X','机器人Y','相机X','相机Y']) 
 
        
      
        
        #---全局变量初始化
 

        #---启动子程序



#---事件     
    def closeEvent(self, event):

        try:
            pass
        except:
            pass
        self.close()
        os._exit(0)
        
#---主界面按钮事件 
    #---自动运行
    def bCalc2Click(self):
        self.sqlChoose(1)
        pass
    def bChooseClick(self):
        global sqlChoose
        self.sqlChoose(0)
        pass

    def bCalcClick(self):  
        global I3
        tRectangle=self.tRectangle.currentText()
        tRectangle1=self.tRectangle1.currentText()
        if tRectangle=="方形":
            tM=float(self.tM.toPlainText())            
            tA=float(self.tA.toPlainText())/1000            
            tB=float(self.tB.toPlainText())/1000
            tL1=float(self.tL1.toPlainText())/1000
            I1=tM*(tA**2+tB**2)/12+tM*tL1**2
           
            print(tM,tA,tB,tL1,I1) 
        if tRectangle=="圆形":
            tM=float(self.tM.toPlainText())
            tR10=float(self.tR10.toPlainText())/1000
            tL1=float(self.tL1.toPlainText())/1000
            I1=tM*tR10**2/2+tM*tL1**2
           
            print(tM,tR10,tL1)
        if tRectangle1=="方形":
            tM1=float(self.tM1.toPlainText())            
            tA1=float(self.tA1.toPlainText())/1000            
            tB1=float(self.tB1.toPlainText())/1000
            tL2=float(self.tL2.toPlainText())/1000
            I2=tM1*(tA1**2+tB1**2)/12+tM1*tL2**2            
            print(tM1,tA1,tB1,tL2) 
        if tRectangle1=="圆形":
            tM1=float(self.tM1.toPlainText())
            tR11=float(self.tR11.toPlainText())/1000
            tL2=float(self.tL2.toPlainText())/1000
            I2=tM1*tR11**2/2+tM1*tL2**2
            
            print(tM1,tR11,tL2)
        I3=I1+I2
        I3=round(I3,3)
        self.tI.setText(str(I3))
        print(I3)

        pass

    def bUpdateClick(self):  
        global value,result
        
        for i in range(0,17) :   
            newItem=QTableWidgetItem("")
            self.tDetail1.setItem(i,1,newItem)
        for i in range(16,34) :   
            newItem=QTableWidgetItem("")
            self.tDetail2.setItem(i-16,1,newItem)
        for i in range(34,38) :   
            newItem=QTableWidgetItem("")
            self.tDetail3.setItem(i-34,1,newItem)
            
        row=self.tResult.currentRow()
        currentResult=result[row-1]
        cursor.execute("select * from para where 型号=?",(currentResult,))
        detailResult = cursor.fetchall()    
        detailResult=detailResult[0]
        detailResult=[str(a) for a in detailResult]
        print(detailResult)
        if detailResult[1]=="RH-12FRH70XX/M/C" or"RH-12FRH85XX/M/C"or"RH-12FRH55XX/M/C"or"RH-20FRH100XX/M/C"or"RH-20FRH85XX/M/C":
            print(0)
        if detailResult[1]=="RH3FRHR3515W" or"RH3FRHR3515"or"RH3FRHR3512C":
            print(0)
        if detailResult[1]=="RH-6FRH55XX/M/C" or"RH-6FRH45XX/M/C"or"RH-6FRH35XX/M/C":
            print(0)
        if detailResult[1]=="RH-3FRH4515" or"RH-3FRH3515"or"RH-3FRH5515":
            print(0)
        if detailResult[1]=="RV-20FR":
            print(0)
        if detailResult[1]=="RV-13FRL"or"RV-13FR":
            print(0)
        if detailResult[1]=="RV-7FRL"or"RV-7FR":
            print(0)
        if detailResult[1]=="RV-7FRLL":
            print(0)
        if detailResult[1]=="RV-4FRL"or"RV-4FR":
            print(0)
        if detailResult[1]=="RV-2FRL"or"RV-2FR":
            print(0)
            

        for i in range(0,17) :   
            newItem=QTableWidgetItem(detailResult[i+1])
            self.tDetail1.setItem(i,1,newItem) 
           
            
        for i in range(16,34) :   
            newItem=QTableWidgetItem(detailResult[i+2])
            self.tDetail2.setItem(i-16,1,newItem)   
        for i in range(34,38) :   
            newItem=QTableWidgetItem(detailResult[i+2])
            self.tDetail3.setItem(i-34,1,newItem)      
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
    
#---F选型功能
    def sqlChoose(self,num):
        global  cursor, p ,conn  ,value,result
        for i in range(20) :   
            newItem=QTableWidgetItem("")
            self.tResult.setItem(i,1,newItem)               
        load=int(self.tLoad.toPlainText())
        mod=self.tMod.currentText()
        r=int(self.tR.toPlainText())
        print(mod,load,type(mod))
        if num==0:
            cursor.execute("select * from para where 机器人类型=? AND 最大负载>=? AND 最大动作半径>=? ",(mod,load,r,))
        if num==1:
            float(I3)
            cursor.execute("select * from para where 机器人类型=? AND 最大负载>=? AND 最大动作半径>=? AND 最大惯量>=?",(mod,load,r,I3))
            print(I3)
        value = cursor.fetchall()          
#        print(value)
        countValue=len(value)
        if countValue>=0:
            result=[va[1] for va in value]        
            print(result)
            
        for i in range(0,len(result)) :   
            newItem=QTableWidgetItem(result[i])
            self.tResult.setItem(i,1,newItem) 
            


#---F图片转换
    def toPixImg(self,img1):
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        pixImg=QPixmap(QPixmap.fromImage(qimag1))
        return pixImg
                          
#---F QT界面刷新程序         
    def GUIfresh(self):                                
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
            

  
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApp()
 #   visionWindow=Vison()
  #  windowConn()
#    mainWindow.show()
    app.setActiveWindow(mainWindow)
    mainWindow.show()
#    mainWindow.showMaximized() 
#    mainWindow.showFullScreen() 
    sys.exit(app.exec_())

