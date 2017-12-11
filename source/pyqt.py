# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:50:50 2017

@author: Administrator
"""

import sys  
from PyQt5 import QtWidgets  
  
  
#pyqt窗口必须在QApplication方法中使用  
app=QtWidgets.QApplication(sys.argv)  
  
  
label=QtWidgets.QLabel("<p style='color: red; margin-left: 20px'><b>hell world</b></p>")      #qt支持html标签，强大吧  
#有了实例，就需要用show()让他显示  
label.show()  
  
  
sys.exit(app.exec_())                                 