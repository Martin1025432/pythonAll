# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 08:31:21 2017

@author: Administrator
"""

# In[ ]:

#!/usr/bin/env python

from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
import time 
import win32api,win32con  
import sqlite3
import os, sys
import pickle 
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        global valued,cursor,conn
        conn = sqlite3.connect("sensopart.db")
        cursor = conn.cursor()
        cursor.execute('select * from para where name=?', ('ip',) )       
        valued = cursor.fetchall()
        Frame.__init__(self, master)
        self.master.title('sensopart调焦软件')
        self.master.geometry('274x238')
        self.createWidgets()

        


        
    def createWidgets(self):
        global valued
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.Frame2 = LabelFrame(self.top, text='自动调焦')
        self.Frame2.place(relx=0.058, rely=0.739, relwidth=0.821, relheight=0.239)

        self.Frame1 = LabelFrame(self.top, text='手动点动调焦')
        self.Frame1.place(relx=0.058, rely=0.235, relwidth=0.85, relheight=0.408)

        self.IPVar = StringVar(value=valued[0][1])
        self.IP = Entry(self.top, text='Text1', textvariable=self.IPVar)
        self.IP.place(relx=0.409, rely=0.054, relwidth=0.471, relheight=0.105)

        self.style.configure('Label1.TLabel',anchor='w')
        self.Label1Var =StringVar()
        self.Label1 = Label(self.top, text= "提示信息：",textvariable=self.Label1Var, style='Label1.TLabel')
        self.Label1.place(relx=0.409, rely=0.154, relwidth=0.471, relheight=0.105)
        
        self.con = Button(self.top, text='连接相机', command=self.con_Cmd)
        self.con.place(relx=0.058, rely=0.067, relwidth=0.266, relheight=0.11)
        
        self.auto = Button(self.Frame2, text='运行', command=self.auto_Cmd)
        self.auto.place(relx=0.427, rely=0.20, relwidth=0.324, relheight=0.7)

        self.manual = Button(self.Frame1, text='运行', command=self.manual_Cmd)
        self.manual.place(relx=0.412, rely=0.4, relwidth=0.313, relheight=0.34)

        self.cw = Radiobutton(self.Frame1, text='反转', value=1,command=self.cw_Cmd)
        self.cw.place(relx=0.103, rely=0.66, relwidth=0.21, relheight=0.275)

        self.ccw = Radiobutton(self.Frame1, text='正转', value=0,command=self.ccw_Cmd)
        self.ccw.place(relx=0.103, rely=0.257, relwidth=0.21, relheight=0.275)
        
        self.mainloop()
        

        
    def con_Cmd(self, event=None):
        global sentSoc,receiveSoc,cursor,conn
        a=str(self.IPVar.get())
        HOST = str(self.IPVar.get()   )                   #服务器IP

        sentPort = 2006                                     #端口号
        receivePort = 2005 
        BUFSIZ = 1024
        sentAddr = (HOST,sentPort)
        receiveAddr = (HOST,receivePort)

        sentSoc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字
        receiveSoc= socket(AF_INET , SOCK_STREAM)      #创建TCP/IP套接字
          

        try:
            sentSoc.connect(sentAddr)                        #尝试连接服务器
            receiveSoc.connect(receiveAddr)  
            receiveSoc.setblocking(False)  
            cursor.execute("update para set data=? where name = ?",(a,"ip",))
            conn.commit()
            self.Label1Var.set("连接成功")
            print(HOST)
        except:
            print("连接失败，请查证IP")
            self.Label1Var.set("连接失败，请查证IP")


        
        pass
    
    def ccw_Cmd(self, event=None):
        global sentSoc,receiveSoc
        sentSoc.send(bytes("CJB002",'utf8'))  
        time.sleep(2)              
        sentSoc.send(bytes("TRG",'utf8'))
          
    def cw_Cmd(self, event=None):
        global sentSoc,receiveSoc
        sentSoc.send(bytes("CJB003",'utf8'))  
        time.sleep(2)              
        sentSoc.send(bytes("TRG",'utf8'))          
        
        
   #run
    def auto_Cmd(self, event=None):
        global sentSoc,receiveSoc
        valueAstr=""
        ############清空缓冲区################    
        try:
            valueAstr=str(receiveSoc.recv(1024))
        except:
            print("缓冲区清空完")
        valueA=0
        valueB=2000000
        ############1:获取当前值，并进行第一次移动################ 
        sentSoc.send(bytes("CJB002",'utf8')) 
        time.sleep(2)
        sentSoc.send(bytes("TRG",'utf8')) 
        time.sleep(2)
        
        try:
            valueAstr=str(receiveSoc.recv(1024))
            print(valueAstr)
        except:
            print("error")
            
        valueA=int(valueAstr[2:-1])
        print(valueA)
        count=0
        ############1:正转比较处理##############################  
        while((valueB-valueA)>=-100):
            if(valueB<2000000):
                valueA=valueB
            sentSoc.send(bytes("TRG",'utf8')) 
            valueBstr=""
            time.sleep(1)

            try:
                valueBstr=str(receiveSoc.recv(1024))
                
            except:
                print("error")
            valueB=int(valueBstr[2:-1])  
            print("A=",valueA,"B=",valueB)
            count=count+1
        valueA=0
        valueB=2000000
        ############2:获取当前值，并进行第一次移动################ 
        sentSoc.send(bytes("CJB003",'utf8')) 
        time.sleep(2)
        sentSoc.send(bytes("TRG",'utf8')) 
        time.sleep(2)
#        
#        try:
#            valueBstr=str(receiveSoc.recv(1024))
#            print(valueBstr)
#        except:
#            print("error")
#            
#        valueB=int(valueBstr[2:-1])
#        print(valueB)
#        
#        sentSoc.send(bytes("CJB003",'utf8')) 
#        time.sleep(2)
#        sentSoc.send(bytes("TRG",'utf8')) 
#        time.sleep(2)
#        
#        try:
#            valueBstr=str(receiveSoc.recv(1024))
#            print(valueBstr)
#        except:
#            print("error")
#            
#        valueB=int(valueBstr[2:-1])
#        print(valueB)
        ############2:反转比较处理##############################
        if count>3:
            while((valueB-valueA)>=-400):
                if(valueB<2000000):
                    valueA=valueB
                sentSoc.send(bytes("TRG",'utf8')) 
                valueBstr=""
                time.sleep(1)

                try:
                    valueBstr=str(receiveSoc.recv(1024))
                
                except:
                    print("error")
                valueB=int(valueBstr[2:-1])  
                print("A=",valueA,"B=",valueB)
        if count<3:
            while((valueB-valueA)>=-1000):
                if(valueB<2000000):
                    valueA=valueB
                sentSoc.send(bytes("TRG",'utf8')) 
                valueBstr=""
                time.sleep(1)

                try:
                    valueBstr=str(receiveSoc.recv(1024))
                
                except:
                    print("error")
                valueB=int(valueBstr[2:-1])  
                print("A=",valueA,"B=",valueB)    
        self.Label1Var.set("自动调焦完成")

#        ############3:结束处理##############################              
#            sentSoc.send(bytes("CJB002",'utf8'))  
#            time.sleep(2)              
#            sentSoc.send(bytes("TRG",'utf8'))
#            time.sleep(1) 
#            try:
#                valueBstr=str(receiveSoc.recv(1024))
#                
#            except:
#                print("error")
#            valueB=int(valueBstr[2:-1])
#            print("finalValue:",valueB)
            
            

        
    def manual_Cmd(self, event=None):
            
        sentSoc.send(bytes("TRG",'utf8'))  
        pass

        
    
if __name__ == "__main__":
    top = Tk()
    Application(top)
    try: top.destroy()
    except: pass




