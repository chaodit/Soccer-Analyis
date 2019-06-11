#!/usr/bin/env python
# coding: utf-8

# In[10]:


import json
import pandas as pd
from pandas import Series  
from collections import Counter
import re
import numpy as np
from datetime import datetime, date


# In[11]:


with open('match_performance_m.json', 'r') as json_data:
    Matchs_P = json.load(json_data)
    print ("***** MP ***** : ")
    #print (json.dumps(Matchs_P[0], indent=4))  
with open('player_all.json') as json_data:
    Players = json.load(json_data)
    print("***** Players ***** : " )
    #print(json.dumps(Players[0], indent=4))


# In[12]:


def Avg_Height_Calculator(team):
    allHeight = 0
    num = 0
    for t in team:
        for p in Players:
            if t == p['player_detail']['id']: 
                heightstr = p['player_detail']['detail']['height']
                heightstr = heightstr.replace(',','.').replace('m','')
                if (heightstr != 'null'):
                    num = num + 1
                    height = float(heightstr)
                    allHeight = allHeight + height
                else:
                    height = 0
                #print(height)
                
    if (num != 0):
        avgHeight = allHeight/num
    else:
        avgHeight = 0
    #print(num)
    #print(avgHeight)
    return avgHeight


# In[7]:


def Height_Analysis(Match):
    JsonArray = []
    error = []
    for m in Match:
        url = m['Statistics URL']
        Hometeam = m['Home Starters'] + m['Home Substitutes']
        Awayteam = m['Away Starters'] + m['Away Substitutes']
        Home_Performance = m['Home_performance']
        Away_Performance = m['Away_performance']
        
        h_avg = Avg_Height_Calculator(Hometeam)
        a_avg = Avg_Height_Calculator(Awayteam)

        if (h_avg != 0) and (a_avg != 0):
            jsonObj = {
            "url": url,
            "Home_Performance": Home_Performance,
            "Home_Avg_Height": h_avg,
            "Away_Performance":Away_Performance,
            "Away_Avg_Height": a_avg}
            JsonArray.append(jsonObj)    
    return JsonArray    
    


# In[13]:


H = Height_Analysis(Matchs_P)


# In[16]:


with open('/Users/mac/Dropbox/Soccer/data/player_height.json','w') as outfile:
    
    JsonArray = []
    for a in H:
        jsonObj_h = {
            "performance": a['Home_Performance'],
            "avg_height": a['Home_Avg_Height']
            }
        JsonArray.append(jsonObj_h)
        
        jsonObj_a = {
            "performance": a['Away_Performance'],
            "avg_height": a['Away_Avg_Height'],
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')

