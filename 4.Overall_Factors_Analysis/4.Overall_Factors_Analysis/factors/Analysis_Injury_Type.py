#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
from pandas import Series  
from collections import Counter
import re
import numpy as np
from datetime import datetime, date


# In[2]:


with open('injury_detail.json') as json_data:
    Injurys = json.load(json_data)
    print("***** Injurys ***** : ")
    #print(json.dumps(Injurys[0],indent=4))


# In[3]:


### Injury Type Analysis

def InjuryCount():
    total = [] #Json
    j = 0
    for player in Injurys: 
        if player['injury_information']['detail'] == None:
            str = "No record"
        else:
            for season in player['injury_information']['detail']:
                if season['injury_name'] != None:
                    str = season['injury_name']
                    str = str.replace("Problems","").replace("Injury", "").replace("Surgery", "").replace("problems", "").replace("Fatigue","")
                    str = str.replace("Muscular","Muscle").replace("Torn Muscle Fibre","Muscle").replace("Muscle ","Muscle").replace("Torn muscle bundle","Muscle")
                    str = str.replace("Influenza","Flu").replace("Minor Knock","Knock").replace("Thigh Muscle Strain","Thigh").replace("Tear in the abductor muscle","Adductor")
                    str = str.replace("Thigh MuscleStrain","Thigh").replace("Adductor ","Adductor").replace("groin strain","Groin").replace("Groin ","Groin")
                    str = str.replace("Back trouble","Back ").replace("Sprained ankle","Ankle ")
                    LastDays = season['last_days'].replace(" days","")
                    if  LastDays == "?":
                        LastDays = 0
                    else:
                        LastDays = int(LastDays)
                    total.append({"InjuryName":str, "LastDays": LastDays})
    #print (len(total))# 14452
    totalName = []
    
    for i in total:
        totalName.append(i['InjuryName'])
    
    countName = pd.value_counts(totalName)
    injuryTop30 = np.array(countName[:30].keys())
    
    result = []
    
    for r in injuryTop30:
        result.append({"InjuryName":r, "TotalLastDays": 0, "Count": countName[r], "AvgDays": 0})
    
    for t in total:
        for r in result:
            if t['InjuryName'] == r['InjuryName']:
                r['TotalLastDays'] = t['LastDays'] + r['TotalLastDays']
                r['AvgDays'] = r['TotalLastDays'] / r['Count']
    return(result) 


# In[5]:


Injurys = InjuryCount()


# In[ ]:


with open('/Users/mac/Dropbox/Soccer/data/injury.json','w') as outfile:
    
    JsonArray = []
    for a in naitondiff_result:
        jsonObj_h = {
            "InjuryName": a['Muscle'],
            "Occurrences_num": a['Home_Nation_Diff'],
            "AvgDays":a[]
            }
        JsonArray.append(jsonObj_h)
        
        jsonObj_a = {
            "performance": a['Away_performance'],
            "nation_diff": a['Away_Nation_Diff'],
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')

