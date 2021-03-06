1 Tool P_NTool
2 Close
3 Open "COM1:" As #1         '打开通讯端口COM3、文件1
4 Open "COM3:" As #2
5 Open "COM4:" As #3
6 pvschk=P_02
7 ppick=P_04
8 ph=P_05                              '下方CCD
9 phup=P_15                          '上方CCD
10 Loadset 1,1
11 OAdl On
12 Servo On
13 Wait M_Svo=1
14 M_Out(16)=0
15 PCU=P_Fbc
16 PCU.Z=90
17 Mvs PCU
18 Spd 100
19 *loop1
20 Mov phome
21 Mov ppick,50
22 Mvs ppick
23 Dly 0.2
24 M_Out(16)=1
25 Dly 0.5
26 Mvs ppick,50
27 Wait M_Open(1)=1            '等待COM3打开才执行下一步
28 Print# 1, "TRG"                 '发送TRG，让相机拍照
29 Dly 0.1
30 Input #1,mxup,myup,maup     '接收来至相机的数据
31 pvs1=P_Zero                          '把pvs清零
32 pvs1=PVSCal(1,mxup,myup,maup)      '把
33 pvs1.C=Rad(maup)                     '将角度单位度(deg)转换为弧度(rad)。写进pvs.C
34 pvs1.FL1=pvschk.FL1
35 pvs1.FL2=pvschk.FL2
36 pplace1=pvs1*phup
37 Mov pvschk
38 Dly 0.5
39 Wait M_Open(2)=1
40 Wait M_Open(3)=1
41 Print# 2, "TRG"
42 Dly 0.1
43 Input #3,mx1,my1,ma1
44 mx=mx1/1000
45 my=my1/1000
46 ma=ma1/1000
47 pvs=P_Zero
48 pvs=PVSCal(2,mx,my,ma)
49 pvs.C=Rad(ma)
50 pvs.FL1=pvschk.FL1
51 pvs.FL2=pvschk.FL2
52 phnd=pvs*ph
53 phosei=Inv(phnd)*pvschk
54 pplace2=pplace1*phosei
55 Mvs pplace2,50
56 Mvs pplace2
57 Dly 0.2
58 M_Out(16)=0
59 Dly 0.5
60 Hlt
61 Mvs pplace2,50
62 Dly 0.2
63 Mov phome
64  GoTo *loop1
65  End
pvschk=(+228.292,+51.747,+138.222,+0.000,+0.000,+159.649)(4,0)
ppick=(-120.535,-283.906,+51.221,+0.000,+0.000,+156.092)(0,0)
ph=(+0.031,+6.440,+138.222,+0.000,+0.000,+159.649,+0.000,+0.000)(4,0)
phup=(-0.194,+5.818,+56.589,+0.000,+0.000,+159.651,+0.000,+0.000)(4,0)
PCU=(-120.535,-283.906,+90.000,+0.000,+0.000,+156.092)(0,0)
phome=(+303.862,-230.169,+90.000,+0.000,+0.000,+245.670)(4,0)
pvs1=(+391.915,-218.225,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(4,0)
pplace1=(+391.721,-212.407,+56.589,+0.000,+0.000,+159.651)(4,0)
pvs=(+228.386,+45.236,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(4,0)
phnd=(+228.417,+51.675,+138.222,+0.000,+0.000,+159.649,+0.000,+0.000)(4,0)
phosei=(+0.142,-0.024,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(4,0)
pplace2=(+391.596,-212.336,+56.589,+0.000,+0.000,+159.651,+0.000,+0.000)(4,0)
pplace=(+388.038,-214.268,+56.589,+0.000,+0.000,+159.651)(4,0)
PTL=(+46.010,+58.870,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
PTRG0=(+367.200,+34.410,+320.000,+0.000,+0.000,-2.860,+0.000,+0.000)(4,0)
J1=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)
