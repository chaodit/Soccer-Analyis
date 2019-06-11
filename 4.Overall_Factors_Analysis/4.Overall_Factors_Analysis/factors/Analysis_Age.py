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


with open('matchs.json', 'r') as json_data:
    Matchs_P = json.load(json_data)
    print ("***** MP ***** : ")
    #print (json.dumps(Matchs_P[0], indent=4))  
with open('player_all.json') as json_data:
    Players = json.load(json_data)
    print("***** Players ***** : " )
    #print(json.dumps(Players[0], indent=4))


# In[11]:


### Average Age Analysis

def Age_Calculator(matchDate, dob):
    #Calculate the age of the player, at the time of the match date
    try: 
        birthday = dob.replace(year=matchDate.year)
    except ValueError: 
        # raised when birth date is February 29 and the current year is not a leap year
        birthday = dob.replace(year=matchDate.year, month = dob.month+1, day=1)
    if birthday > matchDate:
        return matchDate.year - dob.year - 1
    else:
        return matchDate.year - dob.year


# In[12]:


#Calculate the average age of the team, at the time of the match date

def Avg_Calculator(matchDate,team):
    age = 0
    num = 0
    for t in team:
        for p in Players:
            if t == p['player_detail']['id']:
                num = num + 1
                dob = p['player_detail']['detail']['dob'].replace("HappyBirthday","")
                    #print(dob)
                age = age + Age_Calculator(matchDate,datetime.strptime(dob,'%b%d,%Y'))
    if num != 0:
        avg = age / num
        return avg
    else:
        return 0


# In[13]:


#Calculate the average age of a match, hometeam and awayteam
    
def Age_MatchTeamAvg(Match):
    JsonArray = []
    error = []
    for m in Match:
        url = m['Statistics URL']
        Hometeam = m['Home Starters'] + m['Home Substitutes']
        Awayteam = m['Away Starters'] + m['Away Substitutes']
        matchDate = datetime.strptime(m['Date'], '%a, %b %d, %Y')
        Home_performance = m['Home_performance']
        Away_performance = m['Away_performance']
        
        h_avg = Avg_Calculator(matchDate,Hometeam)
        a_avg = Avg_Calculator(matchDate,Awayteam)

        if (h_avg != 0) and (a_avg != 0):
            jsonObj = {
            "url": url,
            "matchDate":json.dumps(matchDate, indent=4, default=str),
            "Home_performance": Home_performance,
            "HomeAvgAge": h_avg,
            "Away_performance":Away_performance,
            "AwayAvgAge": a_avg}
            JsonArray.append(jsonObj)    
    return JsonArray


# In[14]:


AgeAnalysis = Age_MatchTeamAvg(Matchs_P)


# In[13]:





# In[21]:


with open('/Users/mac/Dropbox/Soccer/data/player_avgage.json','w') as outfile:
    
    JsonArray = []
    for a in AgeAnalysis:
        jsonObj_h = {
            "performance": a['Home_performance'],
            "avg_age": a['HomeAvgAge']
            }
        JsonArray.append(jsonObj_h)
        
        jsonObj_a = {
            "performance": a['Away_performance'],
            "avg_age": a['AwayAvgAge'],
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')

