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
from Cognex.VisionPro import CogSerializer
from Cognex.VisionPro import CogImage8Grey

def visionproLoad():
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool,myCircleTool2

    try:
        #加载visionpro文件
        QuickBuild = CogSerializer.LoadObjectFromFile('QuickBuild1.vpp')
        #加载工作 
        job=[QuickBuild.Job(i) for i in range(0,4)]
        #加载工具
        myImgTool=[job[i].VisionTool.Tools["Image Source"] for i in range(0,4)]
        myCircleTool=[job[i].VisionTool.Tools["CogFindCircleTool1"] for i in range(0,4)]
        myCircleTool2=[job[i].VisionTool.Tools["CogFindCircleTool2"] for i in range(0,4)]
        myLineTool=[job[i].VisionTool.Tools["CogFindLineTool1"] for i in range(0,4)]
        myPMAlignTool=[job[i].VisionTool.Tools["CogPMAlignTool1"] for i in range(0,4)]
        myFixtureTool=[job[i].VisionTool.Tools["CogFixtureTool1"] for i in range(0,4)]
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
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool,myCircleTool2
    trgDic={"pSheet":0,"pPlate":1,"nSheet":2,"nPlate":3}
    imgDic={"pSheet":"arrayBmp0.bmp","pPlate":"arrayBmp1.bmp","nSheet":"arrayBmp2.bmp","nPlate":"arrayBmp3.bmp"}
    score={"result":0,"PMA":0,"circle":0,"line":1}
    
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
        myPMAlignTool[trgDic[target]].InputImage=CogImage8Grey1
     
        

       # myFixtureTool[trgDic[target]].InputImage=toVisionproImg(imgDic[target]) 
        #运行检测算法
        myPMAlignTool[trgDic[target]].Run()
        
        try:
            count=myPMAlignTool[trgDic[target]].Results.Count
        except:
            count=0
#            myPMAlignTool[trgDic[target]].InputImage.Dispose(True)
#            myPMAlignTool[trgDic[target]].Dispose(True)
#            myPMAlignTool=[job[i].VisionTool.Tools["CogPMAlignTool1"] for i in range(0,4)]
        if count>0:
            myFixtureTool[trgDic[target]].InputImage=CogImage8Grey1 
            score["PMA"]=1
            myFixtureTool[trgDic[target]].Run()
            myCircleTool[trgDic[target]].Run()
            #myLineTool[trgDic[target]].Run()
           
            try:
                x=round(float(myCircleTool[trgDic[target]].Results.GetCircle().CenterX+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationX),3)
                y=round(float(myCircleTool[trgDic[target]].Results.GetCircle().CenterY+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationY),3)
                r=round(float(myCircleTool[trgDic[target]].Results.GetCircle().Radius),3)
                score["circle"]=1
                circle=[(x,y),r]
                print( myCircleTool[trgDic[target]].Results.GetCircle().CenterX,myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationX)
            except Exception as e:
                print(str(e))
                score["circle"]=0
                circle=[(0,0),0]
#            try:    
#                Lx0 = int(myLineTool[trgDic[target]].Results.GetLineSegment().StartX+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationX)
#                Ly0 = int(myLineTool[trgDic[target]].Results.GetLineSegment().StartY+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationY)
#                Lx1 = int(myLineTool[trgDic[target]].Results.GetLineSegment().EndX+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationX)
#                Ly1 = int(myLineTool[trgDic[target]].Results.GetLineSegment().EndY+myPMAlignTool[trgDic[target]].Results[0].GetPose().TranslationY)
#                Langle = round(myLineTool[trgDic[target]].Results.GetLine().Rotation,3);
#                score["line"]=1
#                line=[(Lx0,Ly0),(Lx1,Ly1),Langle]
#                print(line)
#            except Exception as e:
#                print(str(e))
#                score["line"]=0
#                line=[(0,0),(0,0),0]
            score["result"]=score["PMA"]&score["circle"]&score["line"]
            line=[(0,0),(0,0),0]
            myFixtureTool[trgDic[target]].OutputImage.Dispose(True)            
            CogImage8Grey1.Dispose(False) 
        
        #成功返回1，圆心，半径，   线段的起点，终点，角度
        
            return score["circle"],circle
        else:
            score["PMA"]=0
            line=[(0,0),(0,0),0]
            circle=[(0,0),0]
            return score["circle"],circle

        #运算要返回的结果

    except Exception as e:
#    except:
            print(str(e))
            #失败返回-1
            myFixtureTool[trgDic[target]].OutputImage.Dispose(True)
            CogImage8Grey1.Dispose(False)
            return -1,str(e),"error" 
    
def simpleFindCircle(target):
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool,myCircleTool2
    trgDic={"pSheet":0,"pPlate":1,"nSheet":2,"nPlate":3}
    imgDic={"pSheet":"arrayBmp0.bmp","pPlate":"arrayBmp1.bmp","nSheet":"arrayBmp2.bmp","nPlate":"arrayBmp3.bmp"}
    score={"result":0,"PMA":0,"circle":0,"line":0}
    
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
        myCircleTool2[trgDic[target]].InputImage=CogImage8Grey1             
       # myFixtureTool[trgDic[target]].InputImage=toVisionproImg(imgDic[target]) 
        #运行检测算法
        myCircleTool2[trgDic[target]].Run()        
        try:
            x=round(float(myCircleTool2[trgDic[target]].Results.GetCircle().CenterX),3)
            y=round(float(myCircleTool2[trgDic[target]].Results.GetCircle().CenterY),3)
            r=round(float(myCircleTool2[trgDic[target]].Results.GetCircle().Radius),3)
            score["circle"]=1
            score["result"]=1
            circle=[(x,y),r]
                
        except Exception as e:
            print(str(e))
            score["circle"]=0
            score["result"]=0
            circle=[(0,0),0]          
        CogImage8Grey1.Dispose(False)         
        #成功返回1，圆心，半径，   线段的起点，终点，角度        
        return  score["circle"],circle
    except Exception as e:
#    except:
            print(str(e))
            #失败返回-1
            
            CogImage8Grey1.Dispose(False)
            return -1,str(e),"error" 
        
        
def simpleFindLine(target):
    global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool,myCircleTool2
    trgDic={"pSheet":0,"pPlate":1,"nSheet":2,"nPlate":3}
    imgDic={"pSheet":"arrayBmp0.bmp","pPlate":"arrayBmp1.bmp","nSheet":"arrayBmp2.bmp","nPlate":"arrayBmp3.bmp"}
    score={"result":0,"PMA":0,"circle":0,"line":0}
    
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
        myLineTool[trgDic[target]].InputImage=CogImage8Grey1             
       # myFixtureTool[trgDic[target]].InputImage=toVisionproImg(imgDic[target]) 
        #运行检测算法
        myLineTool[trgDic[target]].Run()        
        try:
            Lx0 = round(float(myLineTool[trgDic[target]].Results.GetLineSegment().StartX),3)
            Ly0 = round(float(myLineTool[trgDic[target]].Results.GetLineSegment().StartY),3)
            Lx1 = round(float(myLineTool[trgDic[target]].Results.GetLineSegment().EndX),3)
            Ly1 = round(float(myLineTool[trgDic[target]].Results.GetLineSegment().EndY),3)
            Langle = round(myLineTool[trgDic[target]].Results.GetLine().Rotation,3)
            score["line"]=1
            line=[(Lx0,Ly0),(Lx1,Ly1),Langle]

                
        except Exception as e:
            print(str(e))
            score["line"]=0
            score["result"]=0
            line=[(0,0),(0,0),0]          
        CogImage8Grey1.Dispose(False)         
        #成功返回1，圆心，半径，   线段的起点，终点，角度        
        return score["line"],line
    except Exception as e:
#    except:
            print(str(e))
            #失败返回-1
            
            CogImage8Grey1.Dispose(False)
            return -1,str(e),"error" 



    
global myCircleTool,myLineTool,myPMAlignTool,myFixtureTool,job,myImgTool,myCircleTool2
def test():
    b=win32api.MessageBox(0, "这是一个测试消息", "消息框标题",win32con.MB_OK)
    print(b) 
    
if __name__ == "__main__":
    a=visionproLoad()
    circle=find("pSheet")  
#    line=simpleFindLine("pPlate") 
    print(circle)
    pass
    
      
    


    
   

        
        
        























