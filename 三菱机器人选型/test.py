# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 09:40:36 2018

@author: Administrator
"""

import sqlite3

conn = sqlite3.connect("robot.db")
cursor = conn.cursor()

cursor.execute("select * from para where 机器人类型='六轴' AND 型号='RV-20FR'" )
value = cursor.fetchall()  
       # print(value)
#dictPara={}
#for i in range(len(value)):
#    dictPara[value[i][0]]=str(value[i][1])    