# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:48:08 2018

@author: Administrator
"""

'M_01模式选择 (100进入工具坐标标定模式, 200进入自动模式, 300进入手动模式, 400进入视觉坐标标定模式，500进入当前位置标定模式,1000PH标定模式)
'M_02模式参数1
'M_03模式参数2
'M_04模式参数3
'M_05模式占用标志
'====================================================================
'初始化参数
M500=0
M_01# = 0
M_02# = 0
M_03# = 0
M_04# = 0
M_05# = 0
M102=10
'If M_Psa(2)=0 Then GoTo *LblRun
'*Lbl1
'XLoad 2,"SELECTTHREAD"
'*L30:If C_Prg(2)<>"SELECTTHREAD" Then GoTo *L30
'XRun 2
'Wait M_Run(2)=1
'Dly 1
'*LblRun
'If M_Run(2)=0 Then XRun 2
'Wait M_Run(2)=1
*LSTR
Select M_01#
'====================================================================
'自动模式
'==================================
Case 200
M_05#=1
Dly 0.1
Tool TooL0
Close
Open "COM3:" As #1            '打开通讯端口COM1、文件1
Spd 800
Ovrd 40
Dly 0.2
Loadset 1,1
OAdl On
Servo On
Wait M_Svo=1
M_Out(16)=0
PCU=P_Fbc
PCU.Z=Psafety.Z
Mvs PCU
Mvs Psafety
*loop1
m101=0
*loopDown
Mov PICK,50
Mvs PICK
Dly 0.2
M_Out(16)=1
Dly 0.5
Mvs PICK,50
Wait M_Open(1)=1            '等待COM3打开才执行下一步
*loopP
m100=0                            'm100=1时，报警换盖板
'If m101=1 Then GoTo *lSkipUp
'Wait M_Open(1) = 1              '等待COM1打开才执行下一步
'Print# 1, "TRGP",M102                 '发送TRG，让H上面相机拍照
'Dly 0.1
'Input #1,mxup,myup,maup     '接收来至相机的数据
'If mxup=0 Then
'Mvs Psafety
'm100=1
'Hlt
'GoTo *loopP
'EndIf
'm100=0
'pvs1=P_Zero                          '把pvs清零
'pvs1=PVSCal(2,mxup,myup,maup)      '把
'pvs1.C=-maup                    '将角度单位度(deg)转换为弧度(rad)。写进pvs.C
'pvs1.FL1=pvschk.FL1
'pvs1.FL2=pvschk.FL2
'pplace1=pvs1*phup
'*lSkipUp
Mov pvschk
Dly 0.5
Wait M_Open(1)=1
Print# 1, "TRGS",M102
Dly 0.1
Input #1,mx,my,ma
If mx=0 Then
Mvs Psafety
M_Out(16)=0
Dly 0.2
m101=1
GoTo *loopDown
EndIf
m101=0
pvs=P_Zero
pvs=PVSCal(1,mx,my,ma)
pvs.C=ma
pvs.FL1=pvschk.FL1
pvs.FL2=pvschk.FL2
phnd=pvs*ph
phosei=Inv(phnd)*pvschk
pplace2=PUT*phosei
Spd 600
Mvs pplace2,60
Mvs pplace2
Dly 0.2
M_Out(16)=0
Dly 0.2
Spd 600
Hlt
Mvs pplace2,50
Dly 0.2
Mov Psafety
GoTo *loop1
M_05#=0
M_01#=0
Break
'====================================================================
'手动模式
'==================================
''X点动
Case 300
Tool TooL0
M_01# = 0
If (M_02# > 0) And (M_02# <= 100) Then Spd M_02#
If M_02# <= 0 Then Spd 10
If M_02# > 100 Then Spd 10
P20 = P_Fbc
If (M_03# >= -50) And (M_03# <= 50) Then P20.X = P20.X + M_03#
Mvs P20
Break
'==================================
''Y点动
Case 301
Tool TooL0
M_01# = 0
If (M_02# > 0) And (M_02# <= 100) Then Spd M_02#
If M_02# <= 0 Then Spd 10
If M_02# > 100 Then Spd 10
P20 = P_Fbc
If (M_03# >= -50) And (M_03# <= 50) Then P20.Y = P20.Y + M_03#
Mvs P20
Break
'==================================
'Z
Case 302
Tool TooL0
M_01# = 0
If (M_02# > 0) And (M_02# <= 100) Then Spd M_02#
If M_02# <= 0 Then Spd 10
If M_02# > 100 Then Spd 10
P20 = P_Fbc
If (M_03# >= -50) And (M_03# <= 50) Then P20.Z = P20.Z + M_03#
Mvs P20
Break
'==================================
'C
Case 303
Tool TooL0
M_01# = 0
If (M_02# > 0) And (M_02# <= 100) Then Spd M_02#
If M_02# <= 0 Then Spd 10
If M_02# > 100 Then Spd 10
P20 = P_Fbc
If (M_03# >= -50) And (M_03# <= 50) Then P20.C = P20.C + M_03#
Mvs P20
Break
'==================================
''拍照位
Case 306
M_01#=0
Tool TooL0
If (M_02#>0) And (M_02#<=100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=Psafety.Z
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs pvschk,20
Mvs pvschk               'PVSCHK拍照位
Break
'==================================
''取料位
Case 307
M_01#=0
Tool TooL0
If (M_02#>0) And (M_02#<=100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=Psafety.Z
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs PICK ,20
Mvs PICK                     'PICK 上料位
Break
'==================================
''放料位
Case 308
M_01#=0
Tool TooL0
If (M_02#>0) And (M_02#<100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=Psafety.Z
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs PUT,20
Mvs PUT                      'PUT放料位
Break
'==================================
''安全位
Case 309
M_01#=0
Tool TooL0
If (M_02#>0) And (M_02#<100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=Psafety.Z
Mvs P20
Mvs Psafety                'Psafety 安全位
Break
'==================================================================
'读取当前位置并保存
'==================================
'标定取料位
Case 500
Tool TooL0
M_01#=0
PICK=P_Fbc
Dly 0.2
Break
'==================================
'标定拍照位
Case 501
Tool TooL0
M_01#=0
pvschk=P_Fbc
Dly 0.2
Break
'==================================
'标定放料位
Case 502
Tool TooL0
M_01#=0
PUT=P_Fbc
Dly 0.2
Break
'==================================
 '标定安全位
Case 503
Tool TooL0
M_01#=0
Psafety=P_Fbc
Dly 0.2
Break
'====================================================================
 '吸IO ON
Case 504
M_Out(16) = 1
Break
'====================================================================
 '吸IO OfF
Case 505
M_Out(16) = 0
Break
'====================================================================
 'IO2 ON
Case 506
M_Out(15) = 1
Break
'====================================================================
 ''IO2 OfF
Case 507
M_Out(15) = 0
Break
'====================================================================
'==================================
'标定上CCD坐标标定的三个点位
'Case 511
'Tool P_10
'M_01#=0
'PT21=P_Fbc
'Dly 0.2
'Break
'Case 512
'Tool P_10
'M_01#=0
'PT22=P_Fbc
'Dly 0.2
'Break
'Case 513
'Tool P_10
'M_01#=0
'PT23=P_Fbc
'Dly 0.2
'Break
'==================================
'标定下CCD坐标标定的三个点位
Case 521
Tool P_11
M_01#=0
PT31=P_Fbc
Dly 0.2
Break
Case 522
Tool P_11
M_01#=0
PT32=P_Fbc
Dly 0.2
Break
Case 523
Tool P_11
M_01#=0
PT33=P_Fbc
Dly 0.2
Break
'工具坐标标定模式
'==================================
'盖板TOOL      上CCD
'Case 100
'Tool TooL0
'M_01#=0
'Servo On
'Wait M_Svo=1
'P20=P_Fbc
'P20.Z=120
'Mvs P20
'P20.C=PT1.C
'Mov P20
'Mov PT1, 40
'Mvs PT1                'PT1 安全位
''Tool P_NTool
'Break
''作业１
''Hlt
'Case 110
'Tool TooL0
'M_01#=0                   '手编移动机器人到像素中心     之后强制8信号输入
'P100 = PT1
'PT1 = P_Fbc
''P100 = P_Fbc
'PT4.C=P100.C+Rad(90)
'PT4.Z=PT1.Z
''P101 = P100 * (+0.000,+0.000,+0.000,+0.000,+0.000,+90.000)
'Mvs PT1, 40
'Mov PT4, 40
'Mvs PT4
'Break  '旋'Hlt                       '手编再次移动机器人到像素中心
''作业２ 直角坐标下移动X,Y轴到十字标定点
'Case 111
'Tool TooL0
'M_01#=0
'P102 = P_Fbc
'PT4=P_Fbc
'PTL = P_Zero
'PT = Inv(P102)*P100
'PTL.X = (PT.X+PT.Y)/2
'PTL.Y = (-PT.X+PT.Y)/2
'PTL.C=PT.C
'P_10 = PTL
'PT10=P_Fbc
'Tool P_10
'Break
'==================================
'过渡片TOOL      下CCD
Case 120
Tool TooL0
M_01#=0
Servo On
Wait M_Svo=1
P20=P_Fbc
P20.Z=Psafety.Z
Mvs P20
P20.C=PT2.C
Mov P20
Mvs PT2                'PT2 安全位
'Tool P_NTool
'M500=0
Break
'作业１
Case 121            'Hlt                    '手编移动机器人到像素中心     之后强制8信号输入
Tool TooL0
M_01#=0
P100 = PT2
PT2 = P_Fbc
PT3.C=P100.C+Rad(90)
PT3.Z=PT2.Z
'P101 = P100 * (+0.000,+0.000,+0.000,+0.000,+0.000,+90.000)
Mvs PT3                                                      '旋转90度
'M500=M500+1
Break                     '手编再次移动机器人到像素中心
Case 122                          '作业２ 直角坐标下移动X,Y轴到十字标定点
Tool TooL0
M_01#=0
P102 = P_Fbc
PT3=P_Fbc
PTL = P_Zero
PT = Inv(P102)*P100
PTL.X = (PT.X+PT.Y)/2
PTL.Y = (-PT.X+PT.Y)/2
P_11 = PTL
P_11.C=-PT3.C
PT20=P_Fbc
Tool P_11
'M500=M500+1
Break
'视觉坐标标定模式
'==================================
'盖板      上CCD
'Case 400
'''像素标定
'''相机像素点转换为机器人坐标 走N个点  记录机器人位置   与像素点对应写入标定
'M_05#=1
'Servo On
'Wait M_Svo=1
'Tool P_10
'P1=P_Fbc
'P1.Z=100
'Mvs P1
'Mvs Psafety
'Mvs PT21,50
'Def Plt 1,PT21,PT22,PT23, ,3,3,1
'Spd 100
'M11=1                      'M1(计数器 )初始化
'*LOOP10
'PhotoPlace = Plt 1, M11      '计算第M1号的位置
'Mvs PhotoPlace
'Dly 0.2
'Close
'Open "COM3:" As #1
'Dly 0.2
'Print #1,"TRGP"
'Input #1,M4,m5
'M1=PhotoPlace.X
'M2=PhotoPlace.Y
'M3=0
'Dly 0.2
'Print #1,"XY",M1,M2
'Input #1,M3
'Wait M3=1               '读取机器人1号位置坐标，CCD像素坐标
'M11=M11+1               '计数器加算
'Close
'If M11 <=9 Then *LOOP10    '计数在范围内的话，从 *LOOP开始反复
'M_01#=0
'M_05#=0
'Break
'==================================
'过渡片      下CCD
Case 401
''像素标定
''相机像素点转换为机器人坐标 走N个点  记录机器人位置   与像素点对应写入标定
M_05#=1
Servo On
Wait M_Svo=1
Tool P_11
P1=P_Fbc
P1.Z=Psafety.Z
Mvs P1
Mvs Psafety
Def Plt 1,PT31,PT32,PT33, ,3,3,1
Spd 100
M11=1                      'M1(计数器 )初始化
*LOOP11
PhotoPlace = Plt 1, M11      '计算第M1号的位置
Mvs PhotoPlace
Dly 0.2
Close
Open "COM3:" As #1
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=PhotoPlace.X
M2=PhotoPlace.Y
M3=0
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1               '读取机器人1号位置坐标，CCD像素坐标
M11=M11+1               '计数器加算
Close
If M11 <=9 Then *LOOP11    '计数在范围内的话，从 *LOOP开始反复
M_01#=0
M_05#=0
Break
'===================================================================
'计算PH值
'==================================
''上CCD
Case 1000
M_05#=1
Tool TooL0
OAdl On                   '打开最佳加减速控制
Spd 500                    '速度指定100。单位：［mm/s］
P1=P_Fbc
P1.Z=Psafety.Z
Mvs P1
Mvs Psafety
Close
Open "COM3:" As #1            '打开通讯端口COM1、文件1
Wait M_Open(1) = 1              '等待COM1打开才执行下一步
'Print# 1, "TRGP"                   '发送TRG，让相机拍照
'Dly 0.1
'Input #1, mx2, my2, mc2       '接收来至相机的数据mx,my,ma
'pvs2 = P_Zero                       '将pvs0返回到(0,0,0,0,0,0,0,0)(0,0)。
'pvs2 = PVSCal(2, mx2, my2, mc2)  '将视觉传感器输出的像素数据转换成机器人的坐标数据
'pvs2.C = -mc2                  '将ma角度单位度(deg)转换为弧度(rad)。写进pvs0.C
'pvs2.FL1 = put.FL1            '将pvschk.FL1 赋值给pvs0.FL1
'pvs2.FL2 = put.FL2            '将pvschk.FL2 赋值给pvs0.FL2
'phup = Inv(pvs2) * put        '计算从视觉传感器输出位置到抓取位置的修正值PH
'Hlt
Mvs PICK, 50
Mvs PICK
Dly 0.2
M_Out(16) = 1
Dly 0.2
Mvs PICK, 50
Mvs Psafety
Dly 0.2
Mov pvschk              '拍照位PVSCHK
'下CCD=====================================
'Close
'Open "COM3:" As #1           '打开通讯端口COM3、文件2
'Wait M_Open(1) = 1            '等待COM3打开才执行下一步
Print #1, "TRGS"                 '发送TRG，让相机拍照
Dly 0.1
Input #1, mx1, my1, mc1        '接收来至相机的数据mx,my,ma
pvs1 = P_Zero                    '将pvs0返回到(0,0,0,0,0,0,0,0)(0,0)。
pvs1 = PVSCal(1, mx1, my1, mc1)  '将视觉传感器输出的像素数据转换成机器人的坐标数据
pvs1.C = mc1                '将ma角度单位度(deg)转换为弧度(rad)。写进pvs0.C
pvs1.FL1 = pvschk.FL1             '将pvschk.FL1 赋值给pvs0.FL1
pvs1.FL2 = pvschk.FL2             '将pvschk.FL2 赋值给pvs0.FL2
ph = Inv(pvs1)*pvschk          '计算从视觉传感器输出位置到抓取位置的修正值PH
Mov PUT, 50
Mvs PUT, 3
P1=PVSCal(1, 1000, 1000, 0)
p2=PVSCal(1, 1001, 1000, 0)
M1dx=p2.X-P1.X
M1dy=p2.Y-P1.Y
'P1=PVSCal(2, 1000, 1000, 0)
'p2=PVSCal(2, 1001, 1000, 0)
M2dx=1
M2dy=1
Print #1,"PIX",M1dx,M1dy,M2dx,M2dy
Dly 0.2
Close
Dly 0.2
M_01#=0
M_05#=0
Break
'====================================================================
End Select
GoTo  *LSTR
End