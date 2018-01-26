# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:32:50 2018

@author: Administrator
#"""
#
import os, sys

# Open a file
fd = os.open( "test.txt", os.O_RDWR|os.O_APPEND )

# Write one string

line = "this is test\n" 
# string needs to be converted byte object
b = str.encode(line)
os.write(fd, b)

# Close opened file
os.close( fd)

print ("Closed the file successfully!!")
        






