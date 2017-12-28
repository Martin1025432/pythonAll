# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 11:17:29 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-  
# 功能:python连接access2010数据库(.accdb)  
  
import win32com.client
conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.ACE.OLEDB.12.0;DATA SOURCE=C:/test.mdb;'
conn.Open(DSN)

rs = win32com.client.Dispatch(r'ADODB.Recordset')
rs_name = 'sheet'#表名
rs.Open('[' + rs_name + ']', conn, 1, 3)

rs.AddNew()
rs.Fields.Item(1).Value = 'data'
rs.Update()