from __future__ import division
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage
import time
import sqlite3
import pandas
import collections  
import cv2
import dll
from ctypes import *  
#import cv2
import numpy as np
#import time
#from PyQt5 import *


    


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
        
        self.bPplateTrig.clicked.connect(self.bPplateTrigClick)
        self.bNsheetTrig.clicked.connect(self.bNsheetTrigClick)
        self.bNplateTrig.clicked.connect(self.bNplateTrigClick)
        conn = sqlite3.connect("cm08.db")
        cursor = conn.cursor()
        cursor.execute('select * from para'  )

        value = cursor.fetchall()   
        dictPara={}
        for i in range(len(value)):
            dictPara[value[i][0]]=str(value[i][1])
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
        #初始化相机
        sn=[]
        basler=CDLL('vision.dll')
        basler.capIni()
        for i in range(0,4):  
            sizebuffer=basler.outputStr(i)
            print(c_char_p(sizebuffer).value)
            recStr=str(c_char_p(sizebuffer).value)[2:-1]
            sn.append(recStr)



                  

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
       # print(dictPara)
        for key in dictPara:
            cursor.execute("update para set data=? where name = ?",(dictPara[key],key,))        
        conn.commit()
        
    def bRunClick(self): 
        global basler,dictPara,basler,sn
        
         
        
    def bPsheetTrigClick(self):
        global basler,sn,dictPara
        basler.capBmp(sn.index(dictPara['tPsheetSn']))
        img1=cv2.imread('bmpForProcess.bmp')
#        img1Processed=img1.copy()
#        dll.findEdge(180,255,img1,img1Processed,10,3000,10,500000)
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamSheetP.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
    def bPplateTrigClick(self):
        global basler,sn,dictPara
        basler.capBmp(sn.index(dictPara['tPplateSn']))
        img2=cv2.imread('bmpForProcess.bmp')        
#        dll.findEdge(180,255,img2,img2Processed,10,3000,10,500000)
        img2Rgb=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        qimag2=QImage(img2Rgb[:],img2Rgb.shape[1], img2Rgb.shape[0],img2Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamPlateP.setPixmap(QPixmap(QPixmap.fromImage(qimag2))) 
    def bNsheetTrigClick(self):
        global basler,sn,dictPara
        basler.capBmp(sn.index(dictPara['tNsheetSn']))
        img3=cv2.imread('bmpForProcess.bmp')        
#        dll.findEdge(180,255,img2,img2Processed,10,3000,10,500000)
        img3Rgb=cv2.cvtColor(img3,cv2.COLOR_BGR2RGB)
        qimag3=QImage(img3Rgb[:],img3Rgb.shape[1], img3Rgb.shape[0],img3Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamSheetN.setPixmap(QPixmap(QPixmap.fromImage(qimag3))) 
    def bNplateTrigClick(self):
        global basler,sn,dictPara
        basler.capBmp(sn.index(dictPara['tNplateSn']))
        img4=cv2.imread('bmpForProcess.bmp')        
#        dll.findEdge(180,255,img2,img2Processed,10,3000,10,500000)
        img4Rgb=cv2.cvtColor(img4,cv2.COLOR_BGR2RGB)
        qimag4=QImage(img4Rgb[:],img4Rgb.shape[1], img4Rgb.shape[0],img4Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamPlateN.setPixmap(QPixmap(QPixmap.fromImage(qimag4))) 
#子窗口
qtCreatorFile = "visionPara.ui" # Enter file here.导入文件
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值
class Vison(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
#    close_signal = pyqtSignal()
    def __init__(self):
        global  cursor,paraName, paraData ,conn                              #初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        
        cursor.execute('select * from paraVision'  )
        value = cursor.fetchall()   
        dictParaVision={}
        for i in range(len(value)):
            dictParaVision[value[i][0]]=str(value[i][1])
        print(dictParaVision)
#        self.bPsheetTrig.clicked.connect(MyApp.bPsheetTrigClick)
    def handle_click(self):
#        if not self.isVisible():
        self.show()    
def windowConn():    
    mainWindow.bVisionPara.clicked.connect(visionWindow.handle_click)
    visionWindow.bPsheetTrig.clicked.connect(mainWindow.bPsheetTrigClick)    
    
if __name__ == "__main__":
#    cap = cv2.VideoCapture(0)
#    cap.set(3,2592)   
#    cap.set(4,1944)      
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApp()
    visionWindow=Vison()
    windowConn()
    mainWindow.show()
    sys.exit(app.exec_())
