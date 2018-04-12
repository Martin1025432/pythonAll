*LSTART
Wait M_05#=0
Close
Dly 0.1
Open "COM3:" As #2
Dly 0.1
'If M_Open(2) = 0 Then GoTo *LSTART
Wait M_Open(2) = 1
Dly 0.1
Input #2, M_01#, M_02#, M_03#, M_04#
M_06# = M_06# + 1
Close
Dly 0.05
GoTo *LSTART