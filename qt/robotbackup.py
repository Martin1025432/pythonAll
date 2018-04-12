'M_01模式选择 (100进入工具坐标标定模式, 200进入自动模式, 300进入手动模式, 400进入视觉坐标标定模式，500进入当前位置标定模式,1000PH标定模式)
'M_02模式参数1
'M_03模式参数2
'M_04模式参数3
'M_05模式占用标志
'====================================================================
'初始化参数
M500=0
ph1 = P_01                     'ph1下CCD的ph值
ph2 = P_02                     'ph2上CCD的ph值
M_01# = 0
M_02# = 0
M_03# = 0
M_04# = 0
M_05# = 0
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
Tool P_NTool
Close
Open "COM3:" As #1
'pvschk                         拍照位
'pick                           取料位
'ph                             '下方CCD
'phup                          '上方CCD
Loadset 1,1
OAdl On
Servo On
Wait M_Svo=1
M_Out(16)=0
PCU=P_Fbc
PCU.Z=90
Mvs PCU
Spd 100
Mvs Psafety
*loop1
Mvs Psafety
Mvs ppick,50
Mvs ppick
Dly 0.2
M_Out(16)=1
Dly 0.5
Mvs ppick,50
Wait M_Open(1)=1            '等待COM3打开才执行下一步
Print# 1, "TRGSA"                 '发送TRG，让相机拍照
Dly 0.1
Input #1,mxup,myup,maup     '接收来至相机的数据
pvs1=P_Zero                          '把pvs清零
pvs1=PVSCal(1,mxup,myup,maup)      '把
pvs1.C=Rad(maup)                     '将角度单位度(deg)转换为弧度(rad)。写进pvs.C
pvs1.FL1=pvschk.FL1
pvs1.FL2=pvschk.FL2
pplace1=PUT*phup
Mov pvschk
Dly 0.5
Wait M_Open(3)=1
Print# 2, "TRGSA"
Dly 0.1
Input #3,mx,my,ma
pvs=P_Zero
pvs=PVSCal(2,mx,my,ma)
pvs.C=Rad(ma)
pvs.FL1=pvschk.FL1
pvs.FL2=pvschk.FL2
phnd=pvs*ph
phosei=Inv(phnd)*pvschk
pplace2=pplace1*phosei
Mvs pplace2,50
Mvs pplace2
Dly 0.2
M_Out(16)=0
Dly 0.5
Hlt
Mvs pplace2,50
Dly 0.2
Mov phome
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
If (M_02#>0) And (M_02#<=100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=90
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs pvschk,20
Mvs pvschk               'PVSCHK拍照位
Break
'==================================
''取料位
Case 307
M_01#=0
If (M_02#>0) And (M_02#<=100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=90
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs PICK ,20
Mvs PICK                     'PICK 上料位
Break
'==================================
''放料位
Case 308
M_01#=0
If (M_02#>0) And (M_02#<100) Then Spd M_02#
If M_02#<=0 Then Spd 10
If M_02#>100 Then Spd 10
P20=P_Fbc
P20.Z=90
Mvs P20
Mvs Psafety                'Psafety 安全位
Mvs PUT,20
Mvs PUT                      'PUT放料位
Break
'==================================
''伺服 OFF
Case 309
M_01#=0
Servo Off
Break
'==================================
'伺服 ON
Case 310
M_01#=0
Servo On
Break
'==================================================================
'读取当前位置并保存
'==================================
'标定取料位
Case 500
M_01#=0
PICK=P_Fbc
Dly 0.2
Break
'==================================
'标定拍照位
Case 501
M_01#=0
pvschk=P_Fbc
Dly 0.2
Break
'==================================
'标定放料位
Case 502
M_01#=0
PUT=P_Fbc
Dly 0.2
Break
'==================================
 '标定安全位
Case 503
M_01#=0
P_safety=P_Fbc
Dly 0.2
Break
'====================================================================
'工具坐标标定模式
'==================================
'盖板TOOL      上CCD
Case 100
Tool TooL0
M_01#=0
Servo On
Wait M_Svo=1
P20=P_Fbc
P20.Z=120
Mvs P20
P20.C=PT1.C
Mov P20
Mov PT1, 40
Mvs PT1                'PT1 安全位
'Tool P_NTool
Break
'作业１
'Hlt
Case 110
Tool TooL0
M_01#=0                   '手编移动机器人到像素中心     之后强制8信号输入
P100 = PT1
PT1 = P_Fbc
'P100 = P_Fbc
PT4.C=P100.C+Rad(90)
'P101 = P100 * (+0.000,+0.000,+0.000,+0.000,+0.000,+90.000)
Mvs PT1, 40
Mov PT4, 40
Mvs PT4
Break  '旋'Hlt                       '手编再次移动机器人到像素中心
'作业２ 直角坐标下移动X,Y轴到十字标定点
Case 111
Tool TooL0
M_01#=0
P102 = P_Fbc
PT4=P_Fbc
PTL = P_Zero
PT = Inv(P102)*P100
PTL.X = (PT.X+PT.Y)/2
PTL.Y = (-PT.X+PT.Y)/2
PTL.C=PT.C
P_10 = PTL
PT10=P_Fbc
Tool P_10
Break
'==================================
'过渡片TOOL      下CCD
Case 120
Tool TooL0
M_01#=0
Servo On
Wait M_Svo=1
P20=P_Fbc
P20.Z=120
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
'====================================================================
'视觉坐标标定模式
'==================================
'盖板      上CCD
Case 400
''像素标定
''相机像素点转换为机器人坐标 走N个点  记录机器人位置   与像素点对应写入标定
''将一个点移动至视野中心     在视野范围内移动N个点  记录机器人当前位置 和像素点
M_05#=1
Servo On
Wait M_Svo=1
Tool TooL0
Mvs PT10
Tool P_10
Spd 100
P5=P_Fbc                      '十字中心点与视野中心点重合               '保存中心点P1的机器人坐标
P1=P5*(-10.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P2=P5*(+0.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P3=P5*(+10.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P4=P5*(-10.000,+0.000,+0.000,+0.000,+0.000,+0.000)
P6=P5*(+10.000,+0.000,+0.000,+0.000,+0.000,+0.000)
P7=P5*(-10.000,+10.000,+0.000,+0.000,+0.000,+0.000)
P8=P5*(+0.000,+10.000,+0.000,+0.000,+0.000,+0.000)
P9=P5*(+10.000,+10.000,+0.000,+0.000,+0.000,+0.000)
Mvs P1
Close
Open "COM3:" As #1
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P1.X
M2=P1.Y
M3=0
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1                            '读取机器人1号位置坐标，CCD像素坐标
Mvs P2
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P2.X
M2=P2.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P3
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P3.X
M2=P3.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P4
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P4.X
M2=P4.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P5
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P5.X
M2=P5.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P6
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P6.X
M2=P6.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P7
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P7.X
M2=P7.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P8
Dly 0.2
Print #1,"TRGP"
Input #1,M4,m5
M1=P8.X
M2=P8.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P9
Print #1,"TRGP"
Input #1,M4,m5
M1=P9.X
M2=P9.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Close
M_05#=0
M_01#=0
Break
'==================================
'过渡片      下CCD
Case 401
''像素标定
''相机像素点转换为机器人坐标 走N个点  记录机器人位置   与像素点对应写入标定
''将一个点移动至视野中心     在视野范围内移动N个点  记录机器人当前位置 和像素点
M_05#=1
Servo On
Wait M_Svo=1
Tool TooL0
Mvs PT20
Tool P_11
Spd 100
P5=P_Fbc                                             '十字中心点与视野中心点重合      '保存中心点P1的机器人坐标
P1=P5*(-10.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P2=P5*(+0.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P3=P5*(+10.000,-10.000,+0.000,+0.000,+0.000,+0.000)
P4=P5*(-10.000,+0.000,+0.000,+0.000,+0.000,+0.000)
P6=P5*(+10.000,+0.000,+0.000,+0.000,+0.000,+0.000)
P7=P5*(-10.000,+10.000,+0.000,+0.000,+0.000,+0.000)
P8=P5*(+0.000,+10.000,+0.000,+0.000,+0.000,+0.000)
P9=P5*(+10.000,+10.000,+0.000,+0.000,+0.000,+0.000)
Mvs P1
Close
Open "COM3:" As #1
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P1.X
M2=P1.Y
M3=0
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1                  '读取机器人1号位置坐标，CCD像素坐标
Mvs P2
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P2.X
M2=P2.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P3
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P3.X
M2=P3.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P4
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P4.X
M2=P4.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P5
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P5.X
M2=P5.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P6
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P6.X
M2=P6.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P7
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P7.X
M2=P7.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P8
Dly 0.2
Print #1,"TRGS"
Input #1,M4,m5
M1=P8.X
M2=P8.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Mvs P9
Print #1,"TRGS"
Input #1,M4,m5
M1=P9.X
M2=P9.Y
Dly 0.2
Print #1,"XY",M1,M2
Input #1,M3
Wait M3=1
Close
M_01#=0
M_05#=0
Break
'===================================================================
'计算PH值
'==================================
'盖板      上CCD
Case 1000
M_05#=1
P1=P_Fbc
P1.Z=90
Mvs P1
Mvs Psafety
Open "COM3:" As #1            '打开通讯端口COM1、文件1
Wait M_Open(1) = 1              '等待COM1打开才执行下一步
Print# 1, "TRGP"                   '发送TRG，让相机拍照
Dly 0.1
Input #1, mx2, my2, mc2       '接收来至相机的数据mx,my,ma
pvs2 = P_Zero                       '将pvs0返回到(0,0,0,0,0,0,0,0)(0,0)。
pvs2 = PVSCal(1, mx2, my2, mc2)  '将视觉传感器输出的像素数据转换成机器人的坐标数据
pvs2.C = Rad(mc2)                  '将ma角度单位度(deg)转换为弧度(rad)。写进pvs0.C
pvs2.FL1 = PUT.FL1            '将pvschk.FL1 赋值给pvs0.FL1
pvs2.FL2 = PUT.FL2            '将pvschk.FL2 赋值给pvs0.FL2
phup = Inv(pvs2) * PUT        '计算从视觉传感器输出位置到抓取位置的修正值PH
P_01=ph1                           '将ph1赋值给全局变量P_01
P_02=ph2                           '将ph2赋值给全局变量P_02
M_01#=0
M_05#=0
Break
'==================================
'过渡片      下CCD
Case 1001
M_05#=1
Tool P_NTool            '将控制点返回到初始值。(机械I/F位置、法兰面 )
Close                        '关闭全部文件
Loadset 1, 1               '设置，抓手1，工件1
OAdl On                   '打开最佳加减速控制
Spd 100                    '速度指定100。单位：［mm/s］
Servo On                  '伺服使能
Wait M_Svo = 1           '待机直到伺服使能
M_Out(16) = 0            '将输出点16置位0
P1 = P_Fbc                 '将现在位置赋值给P1。
P1.Z = 90                   '将P1的Z轴高度设为90。
Mvs P1
Mvs Psafety
Mov PICK, 50              '上料位PICK
Mvs PICK
Dly 0.2
M_Out(16) = 1
Dly 0.5
Mvs PICK, 50
Dly 0.2
Mov pvschk              '拍照位PVSCHK
Hlt
Dly 0.2
Open "COM3:" As #1           '打开通讯端口COM3、文件2
Wait M_Open(1) = 1            '等待COM2打开才执行下一步
Print #1, "TRGS"                 '发送TRG，让相机拍照
Dly 0.1
Input #1, mx1, my1, mc1        '接收来至相机的数据mx,my,ma
pvs1 = P_Zero                      '将pvs0返回到(0,0,0,0,0,0,0,0)(0,0)。
pvs1 = PVSCal(2, mx1, my1, mc1)  '将视觉传感器输出的像素数据转换成机器人的坐标数据
pvs1.C = Rad(mc1)                 '将ma角度单位度(deg)转换为弧度(rad)。写进pvs0.C
pvs1.FL1 = pvschk.FL1             '将pvschk.FL1 赋值给pvs0.FL1
pvs1.FL2 = pvschk.FL2             '将pvschk.FL2 赋值给pvs0.FL2
ph = Inv(pvs1)*pvschk          '计算从视觉传感器输出位置到抓取位置的修正值PH
M_01#=0
M_05#=0
Break
'====================================================================
End Select
P_03 = PICK       'PICK 上料位
P_04 = pvschk  'PVSCHK 拍照位
P_05 = PUT       'PUT 放料位
GoTo  *LSTR
End