# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:37:44 2022

@author: User
"""

import csv

with open('W sections.csv','r') as csv_file:
    wValues = csv.reader(csv_file)
    
    for line in wValues:
        print(line)
        
with open('HSS sections.csv','r') as csv_file:
    hssValues = csv.reader(csv_file)
    
    for line in hssValues:
        print(line)