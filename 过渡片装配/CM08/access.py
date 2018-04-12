# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:43:08 2018

@author: Administrator
"""
import win32com.client

#---加载ACCESS产量数据库
conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.ACE.OLEDB.12.0;DATA SOURCE=D:/cm08Database/product.mdb;'
conn.Open(DSN)
        #打开表
rs = win32com.client.Dispatch(r'ADODB.Recordset')
rs_name = 'sheet'#表名
rs.Open('[' + rs_name + ']', conn, 1, 3)        
def accessWrite(JiaJuNumber,CamNumber,SaveDate,CentX,CentY,Radius,R,Result):
#        JiaJuNumber="0"
#        CamNumber="0"
#        SaveDate="2010"
#        CentX="0"
#        CentY="0"
#        Radius="0"
#        Offset="0"
#        Result="OK"
    rs.AddNew()
    rs.Fields.Item(1).Value = JiaJuNumber
    rs.Fields.Item(2).Value = CamNumber
    rs.Fields.Item(3).Value = SaveDate
    rs.Fields.Item(4).Value = CentX
    rs.Fields.Item(5).Value = CentY
    rs.Fields.Item(6).Value = Radius
    rs.Fields.Item(7).Value = R
    rs.Fields.Item(8).Value = Result
    rs.Update()