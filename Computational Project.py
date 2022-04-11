# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:37:44 2022

@author: User
"""

import csv
import math

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
            try:
                row_dict.update({keys[column]:float(W_list[row][column])})
            except ValueError:
                row_dict.update({keys[column]:W_list[row][column]})
        W_values.append(row_dict)
                        
#correct powers of 10 in W_values
for i in range(0,len(W_values)-2):
    W_values[i]["inertia_x"]=10**6*W_values[i]["inertia_x"]
    W_values[i]["inertia_y"]=10**6*W_values[i]["inertia_y"]
    W_values[i]["plastic_x"]=10**3*W_values[i]["plastic_x"] 
    W_values[i]["plastic_y"]=10**3*W_values[i]["plastic_y"]   

def W_local_buckling(dict,fact_comp):
    
    flange_width=dict["flange_width"]
    flange_thickness=dict["flange_thickness"]
    depth=dict["depth"]
    web_thickness=dict["web_thickness"]
    fact_comp_resist=0.9*dict["area"]*Fy
    
    #flange buckling
    flange_buckling=flange_width/2/flange_thickness*math.sqrt(Fy)
    if flange_buckling<145:
        flange_class=1
    elif flange_buckling<170:
        flange_class=2
    elif flange_buckling<340:
        flange_class=3
    else:
        flange_class=4
        
    #web buckling
    web_ratio=(depth-2*flange_thickness)/web_thickness 
    if web_ratio<(1100/math.sqrt(Fy))*(1-0.39*fact_comp/(fact_comp_resist)):
        web_class=1
    elif web_ratio<(1700/math.sqrt(Fy))*(1-0.61*fact_comp/(fact_comp_resist)):
        web_class=2
    elif web_ratio<(1900/math.sqrt(Fy))*(1-0.65*fact_comp/(fact_comp_resist)):
        web_class=3
    else:
        web_class=4
    
    return max(flange_class,web_class)

def euler_buckling_load(length,inertia):
    return math.pi**2*E*inertia/((0.65*length*1000)**2)

def factored_comp_resist(area,euler_buckling_load):
    Fe=euler_buckling_load/area*1000
    coef=(1+math.sqrt(Fy/Fe)**(2*1.34))**(-1/1.34)
    return 0.9*area*Fy/1000*coef

def factored_moment_resist(plastic):
    return 0.9*plastic*Fy/(10**6)  

def beta_value(length,inertia,area):
    euler_stress=euler_buckling_load(length,inertia)/area
    buckling_ratio=math.sqrt(Fy/euler_stress)
    return min(0.6+0.4*buckling_ratio,0.85)

def  U_effect(euler_buckling_load,fact_comp):
    U=0.4/(1-(fact_comp/euler_buckling_load))
    return max(U,1)
      
def W_section_strength(dict,fact_comp,fact_moment):
    
    area=dict["area"]
    inertia_x=dict["inertia_x"]
    inertia_y=dict["inertia_y"]
    plastic_x=dict["plastic_x"]
    plastic_y=dict["plastic_y"]
    
    
    euler_buckling_load_x=euler_buckling_load(length,inertia_x)
    euler_buckling_load_y=euler_buckling_load(length,inertia_y)
    
    fact_comp_resist=factored_comp_resist(area,euler_buckling_load_y)
    U_x=U_effect(euler_buckling_load_x,fact_comp)
    fact_moment_resist_x=factored_moment_resist(plastic_x)
    beta=beta_value(length,inertia_y,area)
    U_y=U_effect(euler_buckling_load_y,fact_comp)
    fact_moment_resist_y=factored_moment_resist(plastic_y)
    
    #first check
    A=fact_comp/fact_comp_resist
    B=(0.85*U_x*fact_moment)/fact_moment_resist_x
    C=beta*U_y*fact_moment/fact_moment_resist_y
    
    #second check
    D=fact_moment/fact_moment_resist_x 
    
    
    return  max(A+B,D)

#takes in W_values and removes beams that are not strong enough. returns W_values
def W_checks(W_values,fact_moment,fact_comp): 
    
    #iterate through W_values and delete values that are not strong enough
    for i in range(len(W_values)-3,-1,-1):
        #local buckling
        buckling_class=W_local_buckling(dict=W_values[i],
                                 fact_comp=fact_comp)
            
        if buckling_class==3 or buckling_class==4:
            del W_values[i]
            
    #section strength 1
    for i in range(len(W_values)-3,-1,-1):    
        section_strth=W_section_strength(dict=W_values[i],
                                         fact_comp=fact_comp,
                                         fact_moment=fact_moment+W_values[i]["moment_self"])
        if section_strth>1:
            del W_values[i]
        
    return W_values

def HSS_local_buckling(dict,fact_comp):
    
    flange_width=dict["height"]
    flange_thickness=dict["wall_thickness"]
    
    #flange buckling
    flange_buckling=flange_width/2/flange_thickness*math.sqrt(Fy)
    if flange_buckling<420:
        flange_class=1
    elif flange_buckling<525:
        flange_class=2
    elif flange_buckling<670:
        flange_class=3
    else:
        flange_class=4
    
    return flange_class

def HSS_section_strength(dict,fact_comp,fact_moment):
    
    area=dict["area"]
    inertia_x=dict["inertia"]
    inertia_y=dict["inertia"]
    plastic_x=dict["plastic"]
    plastic_y=dict["plastic"]
    
    length=height
    
    euler_buckling_load_x=euler_buckling_load(length,inertia_x)
    euler_buckling_load_y=euler_buckling_load(length,inertia_y)
    
    fact_comp_resist=factored_comp_resist(area,euler_buckling_load_y)
    U_x=U_effect(euler_buckling_load_x,fact_comp)
    fact_moment_resist_x=factored_moment_resist(plastic_x)
    beta=beta_value(length,inertia_y,area)
    U_y=U_effect(euler_buckling_load_y,fact_comp)
    fact_moment_resist_y=factored_moment_resist(plastic_y)
    
    #first check
    A=fact_comp/fact_comp_resist
    B=(U_x*fact_moment)/fact_moment_resist_x
    
    #second check
    D=fact_moment/fact_moment_resist_x 
    
    
    return  max(A+B,D)

#takes in HSS_values and removes columns that are not strong enough. returns HSS_values
def HSS_checks(HSS_values,fact_moment,fact_comp): 
    
    #iterate through HSS_values and delete values that are not strong enough
    for i in range(len(HSS_values)-3,-1,-1):
        #local buckling
        buckling_class=HSS_local_buckling(dict=HSS_values[i],
                                          fact_comp=fact_comp)
            
        if buckling_class==3 or buckling_class==4:
            del HSS_values[i]
            
    #section strength 1
    for i in range(len(HSS_values)-3,-1,-1):    
        section_strth=HSS_section_strength(dict=HSS_values[i],
                                           fact_comp=fact_comp,
                                           fact_moment=fact_moment)
        if section_strth>1:
            del HSS_values[i]
        
    return HSS_values


#design load arrays
fact_beam_moment=[0,6.804*2.5+32.5*5**2/12,17.424*2.5+27.5*5**2/12,23.148*2.5+27.5*5**2/12]
fact_beam_comp=[0,18.9,10.6,5.3]
fact_col_moment=[0,34.02,53.1,62.64]
fact_col_comp=[0,162.5,300,437.5]

#constants
Fy=350 #yield strenght of steel in MPa
E=200 #elasticity in GPa
height=3.6 #column height in m
length=5 #beam length in m
    
beams_selected_values=[0]
columns_selected_values=[0]

HSS_values=HSS_checks(HSS_values=HSS_values,
          fact_moment=fact_col_moment[1],
          fact_comp=fact_col_comp[1])
      

#find beams 
for i in range(1,len(fact_beam_moment)):
    beam_select=W_checks(W_values=W_values,
             fact_moment=fact_beam_moment[i],
             fact_comp=fact_beam_comp[i])[0]
    
    beams_selected_values.append(beam_select)
    
    fact_col_comp[i]+=beam_select["compression_self"]
    
   
for i in range(1,4):    
     print("Name is "+str(beams_selected_values[i]["name"]))
#     #print("Area is "+str(beams_selected_values[i]["area"]))
#     #print(beams_selected_values[i])
     print("Strength is "+str(W_section_strength(beams_selected_values[i],fact_beam_comp[i],fact_beam_moment[i])))


#for i in range(1,50):
    #print(i,HSS_values[i]["name"],HSS_section_strength(HSS_values[i],fact_col_comp[1],fact_col_moment[1]))
          
    
#iterate through HSS_values and delete values that are not strong enough
for i in range(1,len(fact_col_moment)):
    col_select=HSS_checks(HSS_values=HSS_values,
              fact_moment=fact_col_moment[i],
              fact_comp=fact_col_comp[i])[0]
    #print(col_select["name"])
    columns_selected_values.append(col_select)
    
    fact_col_comp[i]+=beam_select["compression_self"]
    
for i in range(1,4):    
    print("Name is "+str(columns_selected_values[i]["name"]))
#     #print("Area is "+str(columns_selected_values[i]["area"]))
#     #print(columns_selected_values[i])
    print("Strength is "+str(HSS_section_strength(columns_selected_values[i],fact_col_comp[i],fact_col_moment[i])))

#print(columns_selected_values[1]["name"])

# FCR=factored_comp_resist(beams_selected_values[1]["area"])
# EBL=euler_buckling_load(length,beams_selected_values[1]["inertia_x"])    
# test=U_effect(fact_beam_comp[1],euler_buckling_load=EBL)
# test=factored_moment_resist(beams_selected_values[1]["plastic_x"])
# test=beta_value(length,beams_selected_values[1]["inertia_x"],beams_selected_values[1]["area"])

    
'''    

'''