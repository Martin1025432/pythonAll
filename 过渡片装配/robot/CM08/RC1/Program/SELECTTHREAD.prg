1 *LSTART
2 Wait M_05#=0
3 Close
4 Dly 0.1
5 Open "COM3:" As #2
6 Dly 0.1
7 'If M_Open(2) = 0 Then GoTo *LSTART
8 Wait M_Open(2) = 1
9 Dly 0.1
10 Input #2, M_01#, M_02#, M_03#, M_04#
11 M_06# = M_06# + 1
12 Close
13 Dly 0.05
14 GoTo *LSTART
