#!/usr/bin/env python
# coding: utf-8

# In[13]:


import json
import pymongo
from pymongo import MongoClient
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import Series  
from collections import Counter
import re


# In[14]:


with open('club2016.json') as json_data:
    C2016 = json.load(json_data)
    print("***** C2016 ***** : " )
with open('club2017.json') as json_data:
    C2017 = json.load(json_data)
    print("***** C2017 ***** : " )
with open('club2018.json') as json_data:
    C2018 = json.load(json_data)
    print("***** C2018 ***** : " )
    #print(json.dumps(C2018[10], indent=4))


# In[15]:


clubs2016 = []
clubs2017 = []
clubs2018 = []
for c in C2016:
    clubs2016.append(c['club_information']['name'])

for c in C2017:
    clubs2017.append(c['club_information']['name'])

for c in C2018:
    clubs2018.append(c['club_information']['name'])


# In[24]:


client = MongoClient('localhost',27017)
db = client.soccer

managerinfo = db.managerinfo
goal_details_3s = db.goal_details_3s


# In[45]:


def get_goalkeeper(input_club_name,season):
    gk_in_club = []
    if season == "15/16":
        for c in C2016:
            if c['club_information']['name'] == input_club_name :
                clubID = (c['club_information']['id'] )
                print(clubID)
                for d in c['club_information']['detail']:
                    if d['position'] == "Goalkeeper":
                        gk_in_club.append(d['id'])
    elif season == "16/17":
        for c in C2017:
            if c['club_information']['name'] == input_club_name :
                clubID = (c['club_information']['id'] )
                print(clubID)
                for d in c['club_information']['detail']:
                    if d['position'] == "Goalkeeper":
                        gk_in_club.append(d['id'])
    elif season == "17/18":
        for c in C2018:
            if c['club_information']['name'] == input_club_name :
                clubID = (c['club_information']['id'] )
                #print(clubID)
                for d in c['club_information']['detail']:
                    if d['position'] == "Goalkeeper":
                        gk_in_club.append(d['id'])
   
    
    GK = []
    for p in gk_in_club:
        goalkeeper = list(db.ENG_players.find({"player_detail.id":p}))
       
        for each in goalkeeper[0]['player_detail']['perform']:
            if each['season']== season:
                if each['detail'][0]:
                  
                    pfdata = each['detail'][0]
                    if pfdata['match_plays'] != "-":
                        jsonObj = {
                            "clubID":clubID,
                            "id":goalkeeper[0]['player_detail']['id'],
                            "name":goalkeeper[0]['player_detail']['name'],
                            "position" : "goalkeeper",
                            "nation":goalkeeper[0]['player_detail']['detail']['citizenship'],
                            "height":goalkeeper[0]['player_detail']['detail']['height'],
                            "conceded_goal" : pfdata['conceded goal'],
                            "clean_sheets" : pfdata['clean sheets'],
                            "minutes_played" : pfdata['minutes played'],
                            "match_plays" : pfdata['match_plays'],
                        }
                        GK.append(jsonObj)

        

    max_matchs = 0
    gkObj = {}
    for gk in GK:
        if gk['match_plays'] == "-":
            match_plays = 0
        else:
            match_plays = int(gk['match_plays']) 
        if match_plays > max_matchs:
            max_matchs = match_plays
            gkObj = gk

    return gkObj


# In[28]:


def get_conceded_players(gkObj,season):
    
    if season == "15/16":
        as_home_match = db.ENG2016.find({"Home.Team ID":gkObj['clubID']})
        as_away_match = db.ENG2016.find({"Away.Team ID":gkObj['clubID']})
    elif season == "16/17":
        as_home_match = db.ENG2017.find({"Home.Team ID":gkObj['clubID']})
        as_away_match = db.ENG2017.find({"Away.Team ID":gkObj['clubID']})
    elif season == "17/18":
        as_home_match = db.ENG2018.find({"Home.Team ID":gkObj['clubID']})
        as_away_match = db.ENG2018.find({"Away.Team ID":gkObj['clubID']})
        
    

    conceded_players = []
    as_home_players = []
    as_away_players = []
    hgoals = 0
    agoals = 100
    home_match = 0
    away_match = 0
    
    for item in as_home_match:

        as_home_players = item['Home Starters'] 
        opposite_players = item['Away Starters'] + item['Away Substitutes']

        if gkObj['id'] in as_home_players:
     
            home_match = home_match + 1
            matchdate = datetime.strptime(item['Date'],'%a, %b %d, %Y')
            for ap in opposite_players:
      
                temp = goal_details_3s.find({"goal_information.id":ap})
                for t in temp:
                    if t['goal_information']['detail']!= None:
                        seasons = t['goal_information']['detail']
                        for s in seasons:
                            matchdate2 = datetime.strptime(s['date'],'%m/%d/%y')
                            if matchdate == matchdate2:
                                hgoals = hgoals+1
                                jObj = {
                                    "goal": hgoals,
                                    "matchdate": item['Date'],
                                    "matchurl": item['Match URL'],
                                    "conceded_player_id": t['goal_information']['id'],
                                    "conceded_goal_type": s['type_of_goal']
                                }
                                conceded_players.append(jObj)
    for item in as_away_match:
        as_away_players = item['Away Starters'] 
        opposite_players = item['Home Starters'] + item['Home Substitutes']
        if gkObj['id'] in as_away_players:
            away_match = away_match + 1
            matchdate = datetime.strptime(item['Date'],'%a, %b %d, %Y')

            for ap in opposite_players:
                templist = db.goal_details_3s.find({"goal_information.id":ap})
                for t in templist:
                    if t['goal_information']['detail']!= None:
                        seasons = t['goal_information']['detail']
                        #print(seasons)
                        for s in seasons:
                            matchdate2 = datetime.strptime(s['date'],'%m/%d/%y')
                            if matchdate == matchdate2:
                                agoals = agoals+1
                                jObj = {
                                    "goal": agoals,
                                    "conceded_player_id": t['goal_information']['id'],
                                    "conceded_goal_type": s['type_of_goal']
                                }
                                conceded_players.append(jObj)
    return conceded_players
                             


# In[30]:



def json_most_player(conceded_players):
    IDs = []
    for c in conceded_players:
        IDs.append(c['conceded_player_id'])

    conceded_playersID = pd.value_counts(IDs)
    most_conceded_playe_id = np.array(conceded_playersID[:10].keys())

    most_player =  {
        "name": "conceded_palyer",
        "children": []}
    for c in most_conceded_playe_id:
        player = list(db.ENG_players.find({"player_detail.id":c}))
        tempObj = {
            "name":player[0]['player_detail']['name'],
            "size":int(conceded_playersID[c])
        }
        most_player['children'].append(tempObj) 
    return most_player


# In[32]:



def json_most_type(conceded_players):
    Types = []
    for c in conceded_players:
        Types.append(c['conceded_goal_type'])

    conceded_types = pd.value_counts(Types)
    most_conceded_types =  np.array(conceded_types[:10].keys())

    most_type =  {
        "name": "most_goal_type",
        "children": []}

    for each in most_conceded_types:
        tempObj = {
            "name":each,
            "size":int(conceded_types[each])
        }
        most_type['children'].append(tempObj) 

    return most_type


# In[34]:


def json_most_nation(conceded_players):
    IDs = []
    for c in conceded_players:
        IDs.append(c['conceded_player_id'])
    
    nations =[]
    for c in IDs:
        player = list(db.ENG_players.find({"player_detail.id": c}))
        if len(player) != 0:
            nations.append(player[0]['player_detail']['detail']['citizenship'])

    nations_type = pd.value_counts(nations)
    most_nations_type = np.array(nations_type[:10].keys())     

    most_nation = {
        "name": "nation",
        "children": []}

    for each in most_nations_type:
        tempObj = {
            "name":each,
            "size":int(nations_type[each])
        }
        most_nation['children'].append(tempObj) 

    return most_nation


# In[36]:


def json_most_heights(conceded_players):
    IDs = []
    for c in conceded_players:
        IDs.append(c['conceded_player_id'])
    
    heights = []

    for c in IDs:
        player = list(db.ENG_players.find({"player_detail.id": c}))
        if len(player) != 0:
            heights.append(player[0]['player_detail']['detail']['height'])

    h170 =0
    h175 =0
    h180 =0
    h185 =0
    h190 =0
    h191 =0

    for each in heights:
        h = float(each.replace(",",".").replace("m",""))
        if h < 1.71:
            h170 = h170+1
        elif h < 1.76:
            h175 = h175+1
        elif h < 1.81:
            h180 = h180+1
        elif h < 1.86:
            h185 = h185+1
        elif h < 1.91:
            h190 =h190+1
        elif h >= 1.91:
            h191 = h191+1

    most_height = {
        "name": "height",
        "children": [ {"name": "~170cm","size": h170},
            {"name":"171~175cm", "size": h175},
            {"name":"176~180cm","size": h180},
            {"name":"181~185cm","size": h185},
            {"name":"186~190cm","size": h190},
            {"name":"191cm~","size": h191}]}          

    return most_height


# In[38]:


GKJson2016 = []
for c in clubs2016:
    gkObj = get_goalkeeper(c,"15/16")
    conceded_players = get_conceded_players(gkObj,"15/16")
    
    most_player = json_most_player(conceded_players)
    most_type = json_most_type(conceded_players)
    most_nation = json_most_nation(conceded_players)
    most_heights = json_most_heights(conceded_players)
   
    tempObj = {
        "name": c,
        "children": [
           most_player,
           most_type,
           most_nation,
           most_heights]}
    
    GKJson2016.append(tempObj)


# In[40]:


GKJson2017 = []
for c in clubs2017:
    gkObj = get_goalkeeper(c,"16/17")
    conceded_players = get_conceded_players(gkObj,"16/17")
    
    most_player = json_most_player(conceded_players)
    most_type = json_most_type(conceded_players)
    most_nation = json_most_nation(conceded_players)
    most_heights = json_most_heights(conceded_players)
   
    tempObj = {
        "name": c,
        "children": [
           most_player,
           most_type,
           most_nation,
           most_heights]}
    
    GKJson2017.append(tempObj)


# In[41]:


GKJson2018 = []
for c in clubs2018:
    gkObj = get_goalkeeper(c,"17/18")
    conceded_players = get_conceded_players(gkObj,"17/18")
    
    most_player = json_most_player(conceded_players)
    most_type = json_most_type(conceded_players)
    most_nation = json_most_nation(conceded_players)
    most_heights = json_most_heights(conceded_players)
   
    tempObj = {
        "name": c,
        "children": [
           most_player,
           most_type,
           most_nation,
           most_heights]}
    
    GKJson2018.append(tempObj)


# In[626]:


with open('/Users/mac/Desktop/D3/GK2016/data/GK2016.json','w') as outfile:
    
    outfile.write('[')

    json.dump(GKJson2016[0],outfile)
    
    for a in GKJson2016[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')


# In[627]:


with open('/Users/mac/Desktop/D3/GK2017/data/GK2017.json','w') as outfile:
    
    outfile.write('[')

    json.dump(GKJson2017[0],outfile)
    
    for a in GKJson2017[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')


# In[628]:


with open('/Users/mac/Desktop/D3/GK2018/data/GK2018.json','w') as outfile:
    
    outfile.write('[')

    json.dump(GKJson2018[0],outfile)
    
    for a in GKJson2018[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)
    outfile.write(']')


# In[72]:


GKArray = []
for c in clubs2016:
    gkObj = get_goalkeeper(c,"15/16")
    Obj = {
        "year":"2015",
        "club":c,
        "name":gkObj['name'],
        "height":gkObj['height'],
        "nation":gkObj['nation'],
        "match_plays":gkObj['match_plays'],
        "average_height":int(gkObj['clean_sheets']),
        "total_goals":int(gkObj['conceded_goal'])
    }
    GKArray.append(Obj)
for c in clubs2017:
    gkObj = get_goalkeeper(c,"16/17")
    Obj = {
        "year":"2016",
        "club":c,
        "name":gkObj['name'],
        "height":gkObj['height'],
        "nation":gkObj['nation'],
        "match_plays":gkObj['match_plays'],
        "average_height":int(gkObj['clean_sheets']),
        "total_goals":int(gkObj['conceded_goal'])
    }
    GKArray.append(Obj)
for c in clubs2018:
    gkObj = get_goalkeeper(c,"17/18")
    Obj = {
        "year":"2017",
        "club":c,
        "name":gkObj['name'],
        "height":gkObj['height'],
        "nation":gkObj['nation'],
        "match_plays":gkObj['match_plays'],
        "average_height":int(gkObj['clean_sheets']),
        "total_goals":int(gkObj['conceded_goal'])
    }
    GKArray.append(Obj)
    


# In[73]:


with open('/Users/mac/Desktop/D3/GK.json','w') as outfile:

    json.dump(GKArray[0],outfile)
    for a in GKArray[1:]:
        outfile.write(',\n')
        json.dump(a,outfile)

