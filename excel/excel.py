# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 12:38:20 2017

@author: Administrator
"""

import xlrd
from xlwt import *

data = xlrd.open_workbook('报价.xlsx')

tableData = data.sheets()[0]
dataRows = tableData.nrows#行数
#dataCols = tableData.ncols #列数

tableTool = data.sheets()[1]
toolRows = tableTool.nrows#行数
#Toolcols = tableTool.ncols #列数

#获取索引值,indexValue 客户询价单型号
toolValues=[tableTool.row_values(i) for i in  range(0,toolRows)]
indexValue=[toolValues[i][0] for i in  range(1,toolRows)]

dataValues=[tableData.row_values(i) for i in  range(0,dataRows)]
#bValue   数据库客户型号
bValue=[dataValues[i][1] for i in  range(1,dataRows)]
#cValue   未税价
cValue=[dataValues[i][2] for i in  range(1,dataRows)]
#dValue   品牌
dValue=[dataValues[i][3] for i in  range(1,dataRows)]
#GValue   价格有效期
hValue=[dataValues[i][7] for i in  range(1,dataRows)]
price=[]
brand=[]
day=[]

flag=0
for k in range(0,len(indexValue)):
    flag=0
    for i in range(0,len(bValue)):
        if bValue[i] in str(indexValue[k]):
            brand.append(dValue[i])
            price.append(cValue[i])
            day.append(hValue[i])
            flag=1
            break
    if flag==0:
        brand.append('无法找到数据')
        price.append('无法找到数据')
        day.append('无法找到数据')
          
w = Workbook()

ws = w.add_sheet('报价输出')
tableTool.row_values(0)[0]
for i in range(0,len(tableTool.row_values(0))):
    ws.write(0, i, tableTool.row_values(0)[i])
    
for i in range(0,len(indexValue)):
    ws.write(i+1, 0, indexValue[i])
    
for i in range(0,len(indexValue)):
    ws.write(i+1, 1, price[i])
    
for i in range(0,len(indexValue)):
    ws.write(i+1, 2, brand[i])
    
for i in range(0,len(indexValue)):
    ws.write(i+1, 4, '17')

for i in range(0,len(indexValue)):
    ws.write(i+1, 6, day[i]) 

w.save('output.xls')


