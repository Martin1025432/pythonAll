1 Tool P_NTool                  '工具坐标返回初始值。
2 Close                          '关闭文件
3 Loadset 1,1                       '设置，抓手1，工件1
4 OAdl On                            '打开最佳加减速控制
5 Spd 100
6 Servo On                           '开启伺服
7 Wait M_Svo=1                   '等待 M_Svo等于1才执行下一步
8 PCU=P_Fbc                       '把当前位置P_Fbc写进PCU
9 PCU.Z=90
10 Mvs PCU                           '把当前位置PCU上移到130mm
11 Mov Phome
12 Dly 0.2
13 Hlt
14 ''''''''''''''''''''''''''''''''''''''''''''''                       示教放料位PUT
15 Open "COM1:" As #1         '打开通讯端口COM3、文件1
16 Wait M_Open(1)=1            '等待COM3打开才执行下一步
17 Print# 1, "TRG"                 '发送TRG，让相机拍照
18 Dly 0.1
19 Input #1,mx,my,ma     '接收来至相机的数据
20 pvs0=P_Zero                          '把pvs清零
21 pvs0=PVSCal(1,mx,my,ma)      '把
22 pvs0.C=Rad(ma)                     '将角度单位度(deg)转换为弧度(rad)。写进pvs.C
23 pvs0.FL1=pvschk.FL1
24 pvs0.FL2=pvschk.FL2
25 PH=Inv(pvs0)*pplace
26 P_15=PH
27 Hlt
PCU=(+210.302,-230.169,+90.000,+0.000,+0.000,+245.670)(4,0)
Phome=(+210.302,-230.169,+90.000,+0.000,+0.000,+245.670)(4,0)
pvs0=(+388.232,-220.086,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
pvschk=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
PH=(-0.194,+5.818,+56.589,+0.000,+0.000,+159.651,+0.000,+0.000)(4,0)
pplace=(+388.038,-214.268,+56.589,+0.000,+0.000,+159.651)(4,0)
PPUT=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
PTL2=(+50.030,+3.570,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
PTRG=(+436.930,+760.500,+302.980,+180.000,+0.000,+90.000,+0.000,+0.000)(7,0)
PUT=(+402.068,-235.863,+55.909,+0.000,+0.000,-31.227)(4,0)
PVS=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
PVS1=(+458.190,+765.630,+0.000,+0.000,+0.000,-4.180,+0.000,+0.000)(7,0)
PWK=(+424.400,+742.320,+302.840,+180.000,+0.000,+90.000)(7,0)
