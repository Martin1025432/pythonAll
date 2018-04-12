# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 20:46:46 2018

@author: Administrator
"""
# coding=utf-8

## clr是公共运行时环境，这个模块是与C#交互的核心
import clr
import cv2
import System
import System.Drawing
import math
import win32api,win32con  

## 导入clr时这个模块最好也一起导入，这样就可以用AddReference方法
#import System
clr.FindAssembly('find.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Caliper.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Controls.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Core.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.CorePlus.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Database.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Display.Controls.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.ImageFile.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.ImageProcessing.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.Inspection.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.PixelMap.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.ToolGroup.Controls.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.ToolGroup.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.QuickBuild.Controls.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.QuickBuild.Core.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.QuickBuild.IO.dll')  # 加载c#dll文件
clr.FindAssembly('Cognex.VisionPro.PMAlign.Controls.dll')  # 加载c#dll文件clr.AddReference('Cognex.VisionPro.Caliper')
clr.FindAssembly('Cognex.VisionPro.PMAlign.dll')
clr.FindAssembly('Cognex.VisionPro.CalibFix.Controls.dll')
clr.FindAssembly('Cognex.VisionPro.CalibFix.dll')
clr.AddReference('Cognex.VisionPro')
clr.AddReference('Cognex.VisionPro.ImageFile')
clr.AddReference('Cognex.VisionPro.ToolGroup')
clr.AddReference('Cognex.VisionPro.QuickBuild.Core')
clr.AddReference('Cognex.VisionPro.PMAlign')
clr.AddReference('Cognex.VisionPro.CalibFix')
clr.AddReference('System.Windows')

from System import Array

from Cognex.VisionPro.Caliper import *
from Cognex.VisionPro import *
from Cognex.VisionPro.ImageFile import *
from Cognex.VisionPro.ToolGroup import *


def visionproLoad():
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool

    try:
        #加载visionpro文件
        QuickBuild = CogSerializer.LoadObjectFromFile('QuickBuild1.vpp')
        #加载工作 
        job=[QuickBuild.Job(i) for i in range(0,4)]
        #加载工具
        myImgTool=[job[i].VisionTool.Tools["Image Source"] for i in range(0,4)]
#        myCircleTool=[job[i].VisionTool.Tools["CogFindCircleTool1"] for i in range(0,4)]
#        myLineTool=[job[i].VisionTool.Tools["CogFindLineTool1"] for i in range(0,4)]
#        myPMAlignTool=[job[i].VisionTool.Tools["CogPMAlignTool1"] for i in range(0,4)]
#        myFixtureTool=[job[i].VisionTool.Tools["CogFixtureTool1"] for i in range(0,4)]
        return 1
    except Exception as e:
        print(str(e))
        return -1,str(e)
#def toVisionproImg(bmpPath):
#    curBitmap=System.Drawing.Bitmap(bmpPath)
#    rect=System.Drawing.Rectangle(0, 0, curBitmap.Width, curBitmap.Height)
#    bmpData=curBitmap.LockBits(rect, System.Drawing.Imaging.ImageLockMode.ReadOnly, curBitmap.PixelFormat)
#    IntPtrPixelData = bmpData.Scan0
#    PixelDataBuffer=Array.CreateInstance(System.Byte,curBitmap.Width*curBitmap.Height)
#    System.Runtime.InteropServices.Marshal.Copy(IntPtrPixelData, PixelDataBuffer, 0, PixelDataBuffer.Length)
#    cogImage8Grey1 = CogImage8Grey(curBitmap.Width, curBitmap.Height)
#    Image8GreyIntPtr = cogImage8Grey1.Get8GreyPixelMemory(CogImageDataModeConstants.Read, 0, 0, cogImage8Grey1.Width, cogImage8Grey1.Height).Scan0    
#    System.Runtime.InteropServices.Marshal.Copy(PixelDataBuffer, 0, Image8GreyIntPtr, PixelDataBuffer.Length)
#    curBitmap.Dispose()
#    PixelDataBuffer=''
#    return cogImage8Grey1
                  
def find(target):
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool
    trgDic={"pSheet":0,"pPlate":1,"nSheet":2,"nPlate":3}
    imgDic={"pSheet":"arrayBmp0.bmp","pPlate":"arrayBmp1.bmp","nSheet":"arrayBmp2.bmp","nPlate":"arrayBmp3.bmp"}
    score={"result":0,"PMA":0,"circle":0,"line":0}

    myCircleTool=job[trgDic[target]].VisionTool.Tools["CogFindCircleTool1"]
    myLineTool=job[trgDic[target]].VisionTool.Tools["CogFindLineTool1"] 
    myPMAlignTool=job[trgDic[target]].VisionTool.Tools["CogPMAlignTool1"] 
    myFixtureTool=job[trgDic[target]].VisionTool.Tools["CogFixtureTool1"]  
#    bmp=System.Drawing.Bitmap(imgDic[target])
#    CogImage8Grey1=CogImage8Grey(bmp)
#    bmp.Dispose()
#    myPMAlignTool[trgDic[target]].InputImage=CogImage8Grey1
#    myFixtureTool[trgDic[target]].InputImage=CogImage8Grey1  
#    CogImage8Grey1.Dispose(True)
    
                
    try:
        #加载处理的图片
      #  myPMAlignTool[trgDic[target]].InputImage=toVisionproImg(imgDic[target])
        bmp=System.Drawing.Bitmap(imgDic[target])
        CogImage8Grey1=CogImage8Grey(bmp)
        bmp.Dispose()
#        myPMAlignTool[trgDic[target]].InputImage=CogImage8Grey1
#        myFixtureTool[trgDic[target]].InputImage=CogImage8Grey1  
        myPMAlignTool.InputImage=CogImage8Grey1
        myFixtureTool.InputImage=CogImage8Grey1 
        CogImage8Grey1.Dispose(False)

       # myFixtureTool[trgDic[target]].InputImage=toVisionproImg(imgDic[target]) 
        #运行检测算法
        myPMAlignTool.Run()
        count=myPMAlignTool.Results.Count
        if count>0:
            score["PMA"]=1
        else:
            score["PMA"]=0
        myFixtureTool.Run()
        myCircleTool.Run()
        myLineTool.Run()
        myFixtureTool.OutputImage.Dispose(True)
        

        #运算要返回的结果
        try:
            x=int(myCircleTool.Results.GetCircle().CenterX+myPMAlignTool.Results[0].GetPose().TranslationX)
            y=int(myCircleTool.Results.GetCircle().CenterY+myPMAlignTool.Results[0].GetPose().TranslationY)
            r=int(myCircleTool.Results.GetCircle().Radius)
            score["circle"]=1
            circle=[(x,y),r]
        except Exception as e:
            print(str(e))
            score["circle"]=0
            circle=[(0,0),0]
        try:    
            Lx0 = int(myLineTool.Results.GetLineSegment().StartX+myPMAlignTool.Results[0].GetPose().TranslationX)
            Ly0 = int(myLineTool.Results.GetLineSegment().StartY+myPMAlignTool.Results[0].GetPose().TranslationY)
            Lx1 = int(myLineTool.Results.GetLineSegment().EndX+myPMAlignTool.Results[0].GetPose().TranslationX)
            Ly1 = int(myLineTool.Results.GetLineSegment().EndY+myPMAlignTool.Results[0].GetPose().TranslationY)
            Langle = round(myLineTool.Results.GetLine().Rotation,3);
            score["line"]=1
            line=[(Lx0,Ly0),(Lx1,Ly1),Langle]
        except Exception as e:
            print(str(e))
            score["line"]=0
            line=[(0,0),(0,0),0]
        score["result"]=score["PMA"]&score["circle"]&score["line"]
        myFixtureTool.Dispose()
        myCircleTool.Dispose()
        myLineTool.Dispose()        
        
        #成功返回1，圆心，半径，   线段的起点，终点，角度
        
        return score,circle,line
    except Exception as e:
#    except:
            print(str(e))
            #失败返回-1
            myFixtureTool.Dispose()
            myCircleTool.Dispose()
            myLineTool.Dispose()   
            return -1,str(e),"error" 
    
    
global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool
def test():
    b=win32api.MessageBox(0, "这是一个测试消息", "消息框标题",win32con.MB_OK)
    print(b) 
    
if __name__ == "__main__":
    a=visionproLoad()
    score,circle,line=find("nPlate")  
    print(circle)
    
      
    


    
   

        
        
        























