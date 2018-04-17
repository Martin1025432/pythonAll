1 M_03#=0
2 Close 
3 Open "COM3:" As #1
4 If M_Psa(2)=0 Then *LblRun
5 XLoad 2,"THREAD"
6 *L30:If C_Prg(2)<>"THREAD" Then GoTo *L30
7 XRun 2
8 M10=10
9 Wait M_Run(2)=1
10 *LblRun
11 Wait  M_03#=90
12 XStp 2
13 Wait M_Wai(2)=1
14 XRst 2
15 Dly 0.5
16 XClr 2  
17 M1=100
18 End
