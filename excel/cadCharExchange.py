# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 20:35:02 2018

@author: Administrator
"""

import xlrd
from xlwt import *


data = xlrd.open_workbook('cad.xlsx')

tableData = data.sheets()[0]
dataRows = tableData.nrows#行数
#dataCols = tableData.ncols #列数
dataValues=[tableData.row_values(i) for i in  range(0,dataRows)]
input=[]
for i in range(1,dataRows):
    input.append(dataValues[i][0][0:-1])
out=[]

index=[]
for k in range(len(input)):
    for i in range(len(input[k])):
        if input[k][i]=='/':
            index.append(i)
    output= input[k][0:index[0]] + "↙" +input[k][index[0]+1] + "↙" +input[k][index[0]+2] + input[k][index[0]+3:index[1]]+ "↙" +input[k][index[1]+1] + "↙" +input[k][index[1]+2]
    out.append(output)

#print(out)

w = Workbook()
ws = w.add_sheet('报价输出')
for i in range(dataRows):
    ws.write(i, 0, output)
w.save('output.xls')



