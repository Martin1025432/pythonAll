1 Tool P_NTool
2 pvschk=P_02
3 Close
4 OAdl On
5 Servo On
6 Wait M_Svo=1
7 M_Out(16)=0
8 PCU=P_Fbc
9 PCU.Z=90
10 Mvs PCU
11 Hlt
12 Loadset 1,1
13 Spd 100
14 Mov ppick,50
15 Mvs ppick
16 Dly 0.2
17 M_Out(16)=1
18 Dly 0.5
19 Mvs ppick,50
20 Dly 0.2
21 Mov pvschk
22 Dly 0.2
23 Hlt
24 Open "COM3:" As #2
25 Open "COM4:" As #3
26 Wait M_Open(2)=1
27 Wait M_Open(3)=1
28 Print# 2, "TRG"
29 Dly 0.1
30 Input #3,mx1,my1,ma1
31 mx=mx1/1000
32 my=my1/1000
33 ma=ma1/1000
34 pvs=P_Zero
35 pvs=PVSCal(3,mx,my,ma)
36 pvs.C=Rad(ma)
37 pvs.FL1=pvschk.FL1
38 pvs.FL2=pvschk.FL2
39 ph=Inv(pvs)*pvschk
40 Dly 0.1
41 Hlt
42 P_04=ppick
43 P_05=ph
44  Hlt
45  End
pvschk=(+227.064,+50.886,+138.309,+0.000,+0.000,+0.010)(0,0)
PCU=(+227.064,+50.886,+90.000,+0.000,+0.000,+0.010)(0,0)
ppick=(-120.535,-283.906,+51.221,+0.000,+0.000,+156.092)(0,0)
pvs=(+222.471,+57.710,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
ph=(+4.593,-6.824,+138.309,+0.000,+0.000,+0.010,+0.000,+0.000)(0,0)
pplace=(+454.280,+4.077,+89.115,+0.000,+0.000,+256.573)(4,0)
PTL=(+38.050,+58.530,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
J1=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)
