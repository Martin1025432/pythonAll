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
        self.bChoose.clicked.connect(self.bChooseClick)
        self.bCalc.clicked.connect(self.bCalcClick)     
        self.bUpdate.clicked.connect(self.bUpdateClick)      
                        

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
    def bChooseClick(self):
        self.sqlChoose()
        pass

    def bCalcClick(self):  
        pass

    def bUpdateClick(self):  
        global value,result
        row=self.tResult.currentRow()
        currentResult=result[row-1]
        cursor.execute("select * from para where 型号=?",(currentResult,))
        detailResult = cursor.fetchall()    
        detailResult=detailResult[0]
        detailResult=[str(a) for a in detailResult]
        print(detailResult)


        for i in range(0,16) :   
            newItem=QTableWidgetItem(detailResult[i+1])
            self.tDetail1.setItem(i,1,newItem) 
            
        for i in range(16,33) :   
            newItem=QTableWidgetItem(detailResult[i+2])
            self.tDetail2.setItem(i-16,1,newItem)         
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
    def sqlChoose(self):
        global  cursor, p ,conn  ,value,result
        for i in range(18) :   
            newItem=QTableWidgetItem("")
            self.tResult.setItem(i,1,newItem)               
        load=int(self.tLoad.toPlainText())
        mod=self.tMod.currentText()
        r=int(self.tR.toPlainText())
        print(mod,load,type(mod))
        cursor.execute("select * from para where 机器人类型=? AND 最大负载>=? AND 最大动作半径>=? ",(mod,load,r,))
        value = cursor.fetchall()          
#        print(value)
        countValue=len(value)
        if countValue>0:
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

