1 PUT=P_Fbc
2 PUT.Z=80
3 Mov PUT
4 'Mov PHOME                 'PHOME等待位
5 Mov PPICK, 40              'PPICK上料位
6 Mov PPICK
7 Dly 0.2
8 M_Out(16)=1
9 Mov PPICK, 40
10 Mov PVSCHK              'PVSCHK拍照位
11 Dly 0.2
12 Hlt
13 Close
14 Open "COM3:" As #2
15 Open "COM4:" As #3
16 Wait M_Open(2)=1
17 Wait M_Open(3)=1
18 Print #2, "ORG"
19 Dly 0.1
20 Input #3, Mx1, My1, Mc1
21 Mx=Mx1/1000
22 My=My1/1000
23 Mc=Mc1/10000
24 pvs0=P_Zero
25 pvs0=PVSCal(4, Mx, My, Mc)
26 pvs0.C=Rad(Mc)
27 pvs0.FL1=PVSCHK.FL1
28 pvs0.FL2=PVSCHK.FL2
29 PH=Inv(pvs0)*PVSCHK
30 Dly 0.1
31 Hlt
32 P_30=PPICK                 'PPICK上料位
33 P_31=PVSCHK               'PVSCHK拍照位
34 P_32=PPLACE                'PPLACE下料位
35 P_33=PH
36 Hlt
37 End
PUT=(+411.828,-232.544,+80.000,+0.000,+0.000,+156.176,+0.000,+0.000)(0,0)
PPICK=(-120.814,-290.839,+49.826,+0.000,+0.000,+162.780)(0,0)
PVSCHK=(+226.452,+46.649,+138.222,+0.000,+0.000,+152.534)(0,0)
pvs0=(+225.663,+46.607,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(0,0)
PH=(+0.789,+0.042,+138.222,+0.000,+0.000,+152.534,+0.000,+0.000)(0,0)
PPLACE=(+411.127,-232.593,+56.254,+0.000,+0.000,+152.503)(0,0)
PHOME=(+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000,+0.000)(,)
