1 '-------------------------------------------------------------
2 '-------------------------------------------------------------
3  Loadset 1,1
4  OAdl On
5  Servo On
6  Wait M_Svo=1
7  Ovrd M_NOvrd
8  Spd M_NSpd
9  Accel 100,100
10  Base P_NBase
11  Tool PTL2
12 '=== Open Port ===
13  If M_NvOpen(1)<>1 Then
14    NVOpen "COM2:" As #1
15    Wait M_NvOpen(1)=1
16  EndIf
17  NVLoad #1,"sample.job"
18 '=============
19 'GoSub *Make_PH
20 *Main
21  Mov Phome
22  Dly 0.5
23  NVRun #1,"sample.job"
24  EBRead #1,"",M1,PVS1
25  If M1=0 Then Error 9102
26  PVS=PVS1
27  PVS=PVSCal(1,PVS1.X,PVS1.Y,PVS1.C)
28  PVS.C=PVS1.C
29  PVS.FL1=PWK.FL1
30  PVS.FL2=PWK.FL2
31  PTRG=PVS*PH
32  Mov PTRG,-10
33  Ovrd 10
34  Mvs PTRG
35  Dly 0.5
36  HClose 1
37  Dly 0.5
38  Ovrd M_NOvrd
39  Mvs PTRG,-10
40  Mov PPUT,-10
41  Ovrd 10
42  Mvs PPUT
43  Dly 0.5
44  HOpen 1
45  Dly 0.5
46  Ovrd M_NOvrd
47  Mov PPUT,-10
48  Mov Phome
49  Hlt
50 End
51 '-------------------------------------------------------------
52 *Make_PH
53  '‡@Please teaching position "PWK"
54  '‡APlease teaching position "Phome"
55  Mov Phome   'Vision Trigger Point
56  Dly 0.5
57  NVRun #1,"sample.job"
58  EBRead #1,"",MNUM,PVS0
59  If MNUM=0 Then Error 9100   'Work1 Not Found
60  PVS=PVS0
61  PVS=PVSCal(1,PVS0.X,PVS0.Y,PVS0.C)
62  PVS.C=PVS0.C
63  PVS.FL1=PWK.FL1
64  PVS.FL2=PWK.FL2
65  PH=Inv(PVS)*PWK
66  Hlt
67 Return
PTL2=(+50.030,+3.570,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
Phome=(+424.400,+581.870,+410.680,+180.000,+0.000,+90.000)(7,0)
PVS1=(+458.190,+765.630,+0.000,+0.000,+0.000,-4.180,+0.000,+0.000)(7,0)
PVS=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
PWK=(+424.400,+742.320,+302.840,+180.000,+0.000,+90.000)(7,0)
PTRG=(+436.930,+760.500,+302.980,+180.000,+0.000,+90.000,+0.000,+0.000)(7,0)
PH=(-7.810,-14.360,+311.660,+180.000,+0.000,+91.090,+0.000,+0.000)(7,0)
PPUT=(0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000)(,)
PVS0=(+470.340,+764.420,+0.000,+0.000,+0.000,-1.100,+0.000,+0.000)(7,0)
