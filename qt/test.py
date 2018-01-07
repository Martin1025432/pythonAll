# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:32:50 2018

@author: Administrator
"""
import sqlite3
import collections  
conn = sqlite3.connect("cm08.db")
cursor = conn.cursor()
cursor.execute('select * from para'  )
#        cursor.execute('select * from para ') 
value = cursor.fetchall()   
dictPara = collections.OrderedDict()  
for i in range(len(value)):
    dictPara[value[i][0]]=str(value[i][1])
name=list(dictPara.keys())
value=list(dictPara.values())
    