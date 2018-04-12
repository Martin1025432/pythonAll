# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:58:27 2018

@author: Administrator
"""
def on(data,bit):
    a=[1<<i for i in range(0,16)]
    dataOut=data|a[bit]
    return dataOut
def off(data,bit):
    a=[1<<i for i in range(0,16)]
    b=[0xffff^aValue for aValue in a]
    dataOut=data&b[bit]
    return dataOut

new=on(0,3)
new2=off(2,1)





