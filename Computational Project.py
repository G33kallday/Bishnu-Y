# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:37:44 2022

@author: User
"""

import csv

#open W sections csv file and create W_values
#W_values is a list of dictionaries of properties
with open('W sections.csv','r',encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    W_list=list(csv_reader)
    keys = W_list[0]
    W_values = []
    
    for row in range(1,len(W_list)):
        row_dict={}
        for column in range(0,len(W_list[0])):
            row_dict.update({keys[column]:W_list[row][column]})
        W_values.append(row_dict)
        
#print(W_values[1]["name"])
        
for i in range(0,len(W_values)):
    print(W_values[i]["radius_x"])        



#print(W_values[0])
    
    
    
'''    
with open('HSS sections.csv','r',encoding='utf-8-sig') as csv_file:
    hssValues = csv.reader(csv_file)
    
    #for line in hssValues:
        #print(line)
'''