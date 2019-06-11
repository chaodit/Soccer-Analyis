#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import re
import numpy as np
import nltk
from datetime import datetime, date
#import Ipynb_importer
#import Analysis_Age


# In[2]:


with open('matchs.json', 'r') as json_data:
    Matchs_P = json.load(json_data)
    print ("***** Matchs_P ***** : ")
    #print (json.dumps(Matchs_P[0], indent=4))  

with open('manager_all.json', 'r') as json_data:
    Manager = json.load(json_data)
    print ("***** Manager ***** : ")
    #print (json.dumps(Manager[0], indent=4))      

with open('player_all.json') as json_data:
    Players = json.load(json_data)
    print("***** Players ***** : " )
    #print(json.dumps(Players[0], indent=4))


# In[3]:


# AgeGap Analysisi
def AgeGap_Calculator(matchdate,team,managerID):
    manager_age = 100
    gap_square_all = 0
    num = 0
    
    for m in Manager:
        if managerID == m['manager_detail']['id']:
            dob = m['manager_detail']['detail'][0]['dob'].replace("HappyBirthday","")
            manager_age = Age_Calculator(matchdate,datetime.strptime(dob,'%b%d,%Y'))
    if manager_age == 100:
        return 0

    for t in team:
        for p in Players:
            if t == p['player_detail']['id']:
                num = num + 1
                dob = p['player_detail']['detail']['dob'].replace("HappyBirthday","")
                player_age = Age_Calculator(matchdate, datetime.strptime(dob,'%b%d,%Y'))
                gap_square_all = gap_square_all + np.square(manager_age - player_age)
   
    if num != 0:
        gap = np.sqrt(gap_square_all/num)
        return gap
    else:
        return 0
   


# In[33]:


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


# In[34]:


def AgeGap():
    
    JsonArray = []

    for m in Matchs_P:
        url = m['Statistics URL']
        matchDate = datetime.strptime(m['Date'], '%a, %b %d, %Y')
        Hometeam = m['Home Starters'] + m['Home Substitutes']
        Awayteam = m['Away Starters'] + m['Away Substitutes']

        Home_performance = m['Home_performance']
        Away_performance = m['Away_performance']

        if (len(Hometeam)!=0 and len(Awayteam)!=0):
            Home_ManagerID = m['Home Manager']['ID']
            Away_ManagerID = m['Away Manager']['ID']

            h_avgage = Avg_Calculator(matchDate,Hometeam)
            a_avgage = Avg_Calculator(matchDate,Awayteam)

            Home_agegap = AgeGap_Calculator ( matchDate,Hometeam,Home_ManagerID )
            Away_agegap = AgeGap_Calculator ( matchDate,Awayteam,Away_ManagerID )
            
            if Home_agegap != 0 and Away_agegap != 0:
                jsonObj = {
                    "url": url,
                    "matchDate":json.dumps(matchDate, indent=4, default=str),
                    "Home_performance": Home_performance,
                    "Home_AvgAge": h_avgage,
                    #"Home_ManagerAge": 用不用存manger的年龄？
                    "Home_agegap":Home_agegap,
                    "Away_performance":Away_performance,
                    "Away_AvgAge": a_avgage,
                    #"Away_ManagerAge":
                    "Away_agegap":Away_agegap,
                    }
                JsonArray.append(jsonObj)  
    return JsonArray


# In[35]:


agegap_result = AgeGap()


# In[46]:


#Manager Nationality Similarity
def Naiton_Sim_Calculator(team,managerID):
    all_player = 0
    same_player = 0
    manager_nation = ""
    
    for m in Manager:
        if managerID == m['manager_detail']['id']:
            manager_nation = m['manager_detail']['detail'][0]['citizenship']
    
    for t in team:
        for p in Players:
            if t == p['player_detail']['id']:
                all_player = all_player + 1
                if (p['player_detail']['detail']['citizenship'] == manager_nation):
                    same_player = same_player + 1
    if all_player != 0:
        sim = same_player/all_player
        return sim
    else:
        return 100


# In[54]:


def Naiton_Sim():
    JsonArray = []
    for m in Matchs_P:
            url = m['Statistics URL']
            matchDate = datetime.strptime(m['Date'], '%a, %b %d, %Y')
            Hometeam = m['Home Starters'] + m['Home Substitutes']
            Awayteam = m['Away Starters'] + m['Away Substitutes']

            Home_performance = m['Home_performance']
            Away_performance = m['Away_performance']

            if (len(Hometeam)!=0 and len(Awayteam)!=0):
                Home_ManagerID = m['Home Manager']['ID']
                Away_ManagerID = m['Away Manager']['ID']

                Home_Nation_Sim = Naiton_Sim_Calculator(Hometeam,Home_ManagerID)
                Away_Nation_Sim = Naiton_Sim_Calculator(Awayteam,Away_ManagerID)
                
                if (Home_Nation_Sim!= 100 and Away_Nation_Sim != 100):
                    jsonObj = {
                    "url": url,
                    "matchDate":json.dumps(matchDate, indent=4, default=str),
                    "Home_performance": Home_performance,
                    "Home_Nation_Sim": Home_Nation_Sim,
                    "Away_Nation_Sim": Away_Nation_Sim,
                    "Away_performance": Away_performance,
                    }

                JsonArray.append(jsonObj) 
    return JsonArray
        


# In[55]:


naitonsim_result = Naiton_Sim()


# In[56]:


for n in naitonsim_result:
    if n['Home_Nation_Sim'] == 100:
        print(n['url'])
#https://www.transfermarkt.com/1-fc-koln_bayer-04-leverkusen/index/spielbericht/2704456


# In[36]:


with open('/Users/mac/Dropbox/Soccer/data/manager_ageSimi.json','w') as outfile:
    
    JsonArray = []
    for a in agegap_result:
        jsonObj_h = {
            "performance": a['Home_performance'],
            "playr_avg_age": a['Home_AvgAge'],
            "agegap":a['Home_agegap']
            }
        JsonArray.append(jsonObj_h)
        jsonObj_a = {
            "performance": a['Away_performance'],
            "playr_avg_age": a['Away_AvgAge'],
            "agegap":a['Away_agegap']
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')


# In[58]:


with open('/Users/mac/Dropbox/Soccer/data/manager_nationSimi.json','w') as outfile:
    
    JsonArray = []
    for a in naitonsim_result:
        jsonObj_h = {
            "performance": a['Home_performance'],
            "nation_sim": a['Home_Nation_Sim']
            }
        JsonArray.append(jsonObj_h)
        
        jsonObj_a = {
            "performance": a['Away_performance'],
            "nation_sim": a['Away_Nation_Sim'],
            }
        JsonArray.append(jsonObj_a)

    outfile.write('[')
    json.dump(JsonArray[0],outfile)
    for a in JsonArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')

