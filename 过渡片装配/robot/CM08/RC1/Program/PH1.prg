1 PCU=P_Fbc
2 PCU.Z=90
3 Mvs  PCU
4 Mov PQU,30
5 Mvs PQU
6 M_Out(16)=1
7 Dly 0.5
8 Mvs PQU,30
9 Mov PHONE
10 Dly 0.2
11 Hlt
12 Close
13 Open "COM3:" As #1
14 Open"COM4:"  As #2
15 Print #1,"TRG"
16 Dly 0.1
17 Input #2 ,M1,M2,M3
18 Dly 0.2
19 PH.X=M1/1000
20 PH.Y=M2/1000
21 M3=0
22 PH=P_Zero
23 PH=PVSCal(4,M1/1000,M2/1000,M3/1000)
24 PH.C=Rad(M3)
25 PH.FL1=p1.FL1
26 PH.FL2=p1.FL2
27 Hlt
28 Mov PUT,30
29 Hlt
30 Mov PUT
31 M_Out(16)=0
32 Dly 0.5
33 p1=Inv(PH)*PUT
34 Mvs PUT,30
35 Hlt
36 End
PCU=(+410.691,-232.921,+90.000,+0.000,+0.000,+156.409)(0,0)
PQU=(-120.814,-290.839,+49.826,+0.000,+0.000,+162.780)(0,0)
PHONE=(+226.452,+46.649,+138.222,+0.000,+0.000,+152.534)(0,0)
PH=(+226.334,+41.360,+0.000,+0.000,+0.000,+0.000)(4,0)
p1=(+184.554,-279.585,+56.490,+0.000,+0.000,+156.409)(4,0)
PUT=(+409.301,-227.575,+56.182,+0.000,+0.000,+156.409)(0,0)
P00=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
