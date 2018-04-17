1 'Wait M_05# = 0
2 'Close
3 'Dly 0.1
4 'Open "COM3:" As #1
5 'Wait M_Open(1) = 1
6 'Input #1, M_01#, M_02#, M_03#, M_04#
7 'M_06# = 10
8 *LSARTE
9 Close
10 Dly 0.1
11 Open "COM3:" As #1
12 Wait M_Open(1) = 1
13 Print #1,"ERROR"
14 Input #1, M_01#, M_02#, M_03#, M_04#
15 M_07#=M_07#+1
16 If (M_01#<>3)  Then GoTo  *LSARTE
17 If M_Err=1 Then 
18 Reset Err
19 M_01#=0
20 EndIf
21 Close
