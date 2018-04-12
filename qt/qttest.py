from __future__ import division
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QThread ,  pyqtSignal
from PyQt5.QtWidgets import QFileDialog 
import time
import sqlite3
import pandas
import collections  
import cv2
import dll
from ctypes import * 
import visionpro
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
        self.bSelectDoc.clicked.connect(self.bSelectDocClick)
        self.rInline.setChecked(1)
    def bSelectDocClick(self):
  
        directory1 = QFileDialog.getExistingDirectory(self,  
                                    "选取文件夹",  
                                    "C:/")                                 #起始路径  
        print(directory1)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApp()
    mainWindow.show()
    sys.exit(app.exec_())
