# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 20:46:46 2018

@author: Administrator
"""
# coding=utf-8

## clr是公共运行时环境，这个模块是与C#交互的核心
import clr
#import sys
## 导入clr时这个模块最好也一起导入，这样就可以用AddReference方法
#import System
clr.FindAssembly('find.dll')  # 加载c#dll文件
clr.AddReference('find')
from find import *
a=tool.find()
print(a)















