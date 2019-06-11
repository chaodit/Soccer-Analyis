#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
from pandas import Series  
from collections import Counter
import re
import numpy as np
import nltk
from datetime import datetime, date


# In[3]:


with open('matchs.json', 'r') as json_data:
    Matchs_P = json.load(json_data)
    print ("***** MP ***** : ")
    #print (json.dumps(Matchs_P[0], indent=4))  
with open('player_all.json') as json_data:
    Players = json.load(json_data)
    print("***** Players ***** : " )
    #print(json.dumps(Players[0], indent=4))


# In[14]:


#National Diversity Analysis
def Nation_Div(team):
    nations = []
    j = 0
    error = 0
    for hp in team: 
        for p in Players:
            str = p['player_detail']['id']
            if str == hp:
                nations.append(p['player_detail']['detail']['citizenship'])
    nationsUnique = Series(nations).unique()
    if len(nationsUnique) == 1 :
        diversity = 0
    elif len(nations)==0 :
        diversity = 100
    else:
        diversity = len(nationsUnique) / len(nations)
    return diversity

def Match_NationDiv(Match):
    JsonArray = []
    errorArray = []
    for t in Match:
        url = t['Statistics URL']
        matchID = t['Match_id']
        Hometeam = t['Home Starters'] + t['Home Substitutes']
        Awayteam = t['Away Starters'] = t['Away Substitutes']
        Home_performance = t['Home_performance']
        Away_performance = t['Away_performance']
        hd = Nation_Div(Hometeam)
        ad = Nation_Div(Awayteam)
        
        jsonObj = {
            "url": url,
            "matchID":matchID,
            "Home_performance": Home_performance,
            "HomeNationDiv": hd,
            "Away_performance":Away_performance,
            "AwayNationDiv": ad}
        
        if ((hd != 100)and(ad != 100)):
            JsonArray.append(jsonObj)
        else:
            errorArray.append(jsonObj)
    print ("ERROR MATCHS:")
    print (len(errorArray))
    return JsonArray


# In[15]:


nationDiv = Match_NationDiv(Matchs_P)


# In[18]:


with open('/Users/mac/Dropbox/Soccer/data/nation_div.json','w') as outfile:
    
    JsonArray = []
    for a in nationDiv:
        jsonObj_h = {
            "performance": a['Home_performance'],
            "nation_div": a['HomeNationDiv']
            }
        JsonArray.append(jsonObj_h)
        
        jsonObj_a = {
            "performance": a['Away_performance'],
            "nation_div": a['AwayNationDiv'],
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')


# In[ ]:




