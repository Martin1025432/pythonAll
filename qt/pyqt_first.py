from __future__ import division
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage
import time
import sqlite3
import pandas
import cv2
import dll
#import cv2
import numpy as np
#import time
#from PyQt5 import *
qtCreatorFile = "window.ui" # Enter file here.导入文件

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)#给两个变量赋值

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):             #定义一个类
    def __init__(self):
        global  cursor,paraName, paraData ,conn                              #初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        self.bDataReset.clicked.connect(self.bDataResetClick)
        self.bDataSave.clicked.connect(self.bDataSaveClick)
        self.bRun.clicked.connect(self.bRunClick)
        self.bPsheetTrig.clicked.connect(self.bPsheetTrigClick)
        self.bPplateTrig.clicked.connect(self.bPplateTrigClick)
        self.bNsheetTrig.clicked.connect(self.bNsheetTrigClick)
        self.bNplateTrig.clicked.connect(self.bNplateTrigClick)
        conn = sqlite3.connect("cm08.db")
        cursor = conn.cursor()
        paraName=["tPsheetTotal","tPsheetGood","tPsheetGoodRate","tPsheetBad","tPsheetBadRate","tPsheetFail",
                  "tPplateTotal","tPplateGood","tPplateGoodRate","tPplateBad","tPplateBadRate","tPplateFail",
                   "tNsheetTotal","tNsheetGood","tNsheetGoodRate","tNsheetBad","tNsheetBadRate","tNsheetFail",
                   "tNplateTotal","tNplateGood","tNplateGoodRate","tNplateBad","tNplateBadRate","tNplateFail","tTime"]
        paraData=[self.tPsheetTotal.toPlainText(),
                  self.tPsheetGood.toPlainText(),
                  self.tPsheetGoodRate.toPlainText(),
                  self.tPsheetBad.toPlainText(),
                  self.tPsheetBadRate.toPlainText(),
                  self.tPsheetFail.toPlainText(),
                  self.tPplateTotal.toPlainText(),
                  self.tPplateGood.toPlainText(),
                  self.tPplateGoodRate.toPlainText(),
                  self.tPplateBad.toPlainText(),
                  self.tPplateBadRate.toPlainText(),
                  self.tPplateFail.toPlainText(),
                  self.tNsheetTotal.toPlainText(),
                  self.tNsheetGood.toPlainText(),
                  self.tNsheetGoodRate.toPlainText(),
                  self.tNsheetBad.toPlainText(),
                  self.tNsheetBadRate.toPlainText(),
                  self.tNsheetFail.toPlainText(),
                  self.tNplateTotal.toPlainText(),
                  self.tNplateGood.toPlainText(),
                  self.tNplateGoodRate.toPlainText(),
                  self.tNplateBad.toPlainText(),
                  self.tNplateBadRate.toPlainText(),
                  self.tNplateFail.toPlainText(),
                  self.tTime.toPlainText(),]
        paraDataSet=[]
        
        for i in range(len(paraName)):
            cursor.execute('select * from para where name=?', (paraName[i],) )  
#        cursor.execute('select * from para ') 
            value = cursor.fetchall()                    
            paraDataSet.append(str(value[0][1]))
        print(paraDataSet)
        self.tPsheetTotal.setText(paraDataSet[0])
        self.tPsheetGood.setText(paraDataSet[1])
        self.tPsheetGoodRate.setText(paraDataSet[2])
        self.tPsheetBad.setText(paraDataSet[3])
        self.tPsheetBadRate.setText(paraDataSet[4])
        self.tPsheetFail.setText(paraDataSet[5])
        self.tPplateTotal.setText(paraDataSet[6])
        self.tPplateGood.setText(paraDataSet[7])
        self.tPplateGoodRate.setText(paraDataSet[8])
        self.tPplateBad.setText(paraDataSet[9])
        self.tPplateBadRate.setText(paraDataSet[10])
        self.tPplateFail.setText(paraDataSet[11])
        self.tNsheetTotal.setText(paraDataSet[12])
        self.tNsheetGood.setText(paraDataSet[13])
        self.tNsheetGoodRate.setText(paraDataSet[14])
        self.tNsheetBad.setText(paraDataSet[15])
        self.tNsheetBadRate.setText(paraDataSet[16])
        self.tNsheetFail.setText(paraDataSet[17])
        self.tNplateTotal.setText(paraDataSet[18])
        self.tNplateGood.setText(paraDataSet[19])
        self.tNplateGoodRate.setText(paraDataSet[20])
        self.tNplateBad.setText(paraDataSet[21])
        self.tNplateBadRate.setText(paraDataSet[22])
        self.tNplateFail.setText(paraDataSet[23])
        self.tTime.setText(paraDataSet[24])
                  

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
        global paraName, conn,cursor
        paraData=[self.tPsheetTotal.toPlainText(),
                  self.tPsheetGood.toPlainText(),
                  self.tPsheetGoodRate.toPlainText(),
                  self.tPsheetBad.toPlainText(),
                  self.tPsheetBadRate.toPlainText(),
                  self.tPsheetFail.toPlainText(),
                  self.tPplateTotal.toPlainText(),
                  self.tPplateGood.toPlainText(),
                  self.tPplateGoodRate.toPlainText(),
                  self.tPplateBad.toPlainText(),
                  self.tPplateBadRate.toPlainText(),
                  self.tPplateFail.toPlainText(),
                  self.tNsheetTotal.toPlainText(),
                  self.tNsheetGood.toPlainText(),
                  self.tNsheetGoodRate.toPlainText(),
                  self.tNsheetBad.toPlainText(),
                  self.tNsheetBadRate.toPlainText(),
                  self.tNsheetFail.toPlainText(),
                  self.tNplateTotal.toPlainText(),
                  self.tNplateGood.toPlainText(),
                  self.tNplateGoodRate.toPlainText(),
                  self.tNplateBad.toPlainText(),
                  self.tNplateBadRate.toPlainText(),
                  self.tNplateFail.toPlainText(),
                  self.tTime.toPlainText(),]
        print(paraName,paraData)

        
        for i in range(len(paraName)):            
            cursor.execute("update para set data=? where name = ?",(paraData[i],paraName[i],))        
        conn.commit()
    def bRunClick(self): 
        img1=cv2.imread('apple1.jpeg')
#        img1Processed=img1.copy()
#        dll.findEdge(180,255,img1,img1Processed,10,3000,10,500000)
#        img1Resize=cv2.resize(src=img1,dsize=None,fx=0.2,fy=0.2)
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamSheetP.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
        
        img2=cv2.imread('apple2.jpeg')
#        img1Resize=cv2.resize(src=img1,dsize=None,fx=0.2,fy=0.2)
        img2Rgb=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        qimag2=QImage(img2Rgb[:],img2Rgb.shape[1], img2Rgb.shape[0],img2Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamPlateP.setPixmap(QPixmap(QPixmap.fromImage(qimag2))) 
        
        img3=cv2.imread('apple3.jpeg')
#        img1Resize=cv2.resize(src=img1,dsize=None,fx=0.2,fy=0.2)
        img3Rgb=cv2.cvtColor(img3,cv2.COLOR_BGR2RGB)
        qimag3=QImage(img3Rgb[:],img3Rgb.shape[1], img3Rgb.shape[0],img3Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamSheetN.setPixmap(QPixmap(QPixmap.fromImage(qimag3)))  

        img4=cv2.imread('apple4.jpeg')
#        img1Resize=cv2.resize(src=img1,dsize=None,fx=0.2,fy=0.2)
        img4Rgb=cv2.cvtColor(img4,cv2.COLOR_BGR2RGB)
        qimag4=QImage(img4Rgb[:],img4Rgb.shape[1], img4Rgb.shape[0],img4Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamPlateN.setPixmap(QPixmap(QPixmap.fromImage(qimag4)))           
        
    def bPsheetTrigClick(self):
        img1=cv2.imread('apple1.jpeg')
        img1Processed=img1.copy()
        dll.findEdge(180,255,img1,img1Processed,10,3000,10,500000)
        img1Rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
        qimag1=QImage(img1Rgb[:],img1Rgb.shape[1], img1Rgb.shape[0],img1Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamSheetP.setPixmap(QPixmap(QPixmap.fromImage(qimag1))) 
    def bPplateTrigClick(self):
        img2=cv2.imread('apple2.jpeg')
        img2Processed=img2.copy()
        dll.findEdge(180,255,img2,img2Processed,10,3000,10,500000)
        img2Rgb=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        qimag2=QImage(img2Rgb[:],img2Rgb.shape[1], img2Rgb.shape[0],img2Rgb.shape[1] * 3, QImage.Format_RGB888)
        self.lCamPlateP.setPixmap(QPixmap(QPixmap.fromImage(qimag2))) 
    def bNsheetTrigClick(self):
        pass
    def bNplateTrigClick(self):
        pass
if __name__ == "__main__":
#    cap = cv2.VideoCapture(0)
#    cap.set(3,2592)   
#    cap.set(4,1944)      
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    print('wait')
    sys.exit(app.exec_())
