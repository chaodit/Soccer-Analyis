#!/usr/bin/env python
# coding: utf-8

# In[55]:


import json
import pandas as pd
from pandas import Series  
from collections import Counter
import re
import numpy as np
from datetime import datetime, date


# In[56]:


with open('goal_details_3s.json') as json_data:
    Goals = json.load(json_data)
    print("***** Goals ***** : ")
    print(json.dumps(Goals[0], indent=4))


# In[57]:


def playerGoals():
    JsonArray = []
    totalGames = 0
    for g in Goals:
        url = g['goal_information']["url"]
        playerName = g['goal_information']["name"]
        playerID = g['goal_information']["id"]
        if g['goal_information']['detail']!= None:
            goals = g['goal_information']['detail']
            totalGoals = len(goals)
            goalsProviderTop3 = top3_goal_provider(goals)
            goalsTypesTop3 = top3_goal_type(goals)
            goalsPositionTop3 = top_3_position_goal(goals)
            goals_season = season_goal(goals)
            goals_minute = minute_goal(goals)
            goals_league = league_goal(goals)
        else:
            totalGames = 0
            totalGoals = 0
            goalsTypesTop3 = "Null"
            goalsProviderTop3 = "Null"
            goalsPositionTop3 = "Null"
            goalsTypesTop3 = "Null"
            goals_season = "Null"
            goals_minute = "Null"
            goals_league = "Null"
        jsonObj = {
            "url": url,
            "playerID": playerID,
            "totalgoalGames": totalGames,      
            "totalGoals": totalGoals,
            "goalsTypesTop3": goalsTypesTop3,
            "goalsProviderTop3": goalsProviderTop3,
            "goalPositionTop3": goalsPositionTop3,
            "goalSeason": goals_season,
            "goalsMinute": goals_minute,
            "goalsLeague": goals_league}
        JsonArray.append(jsonObj)
    return JsonArray


# In[58]:


def type_goal(Goals):
    goal_type = dict()
    for detail in Goals:
        type_ = detail['type_of_goal']
        goal_type[type_] = goal_type.get(type_,0) + 1
    return goal_type


# In[59]:


def top3_goal_type(Goals):
    goal_type = type_goal(Goals)
    types = []
    for detail in Goals:
        type_ = detail['type_of_goal'].strip()
        if type_ != '':
            types.append(type_)
    types = pd.value_counts(types).keys()
    if(len(types) < 3):
        return goal_type
    else:
        top_three_goal_type = {types[0]:goal_type[types[0]],
                               types[1]:goal_type[types[1]],
                               types[2]:goal_type[types[2]]}
        return top_three_goal_type


# In[60]:


def season_goal(Goals):
    goal_season = dict()
    for detail in Goals:
        season = detail['season']
        goal_season[season] = goal_season.get(season,0) + 1
    return goal_season


# In[61]:


def minute_goal(Goals):
    goal_minute = dict()
    minute = 0
    for detail in Goals:
        if(len((re.findall(r'([0-9]+)',detail['goal_minute'])))!= 0):
            minute = int(re.findall(r'([0-9]+)',detail['goal_minute'])[0])
        if minute <= 45:
            goal_minute['first half'] = goal_minute.get('first half',0) + 1
        else:
            goal_minute['second half'] = goal_minute.get('second half',0) + 1
    return goal_minute


# In[62]:


def league_goal(Goals):
    goal_league = dict()
    for detail in Goals:
        league = detail['league_name']
        goal_league[league] = goal_league.get(league,0) + 1
    return goal_league


# In[63]:


def goal_provider(Goals):
    goal_provider = dict()
    for detail in Goals:
        provider = detail['provider_id']
        goal_provider[provider] = goal_provider.get(provider,0) + 1
    return goal_provider


# In[64]:


def top3_goal_provider(Goals):
    provider_goal = goal_provider(Goals)
    providers = []
    for detail in Goals:
        provider = detail['provider_id'].strip()
        if provider != 'null':
            providers.append(provider)
    providers = pd.value_counts(providers).keys()
    if(len(providers) < 3):
        return provider_goal
    else:
        top_three_goal_provider = {providers[0]:provider_goal[providers[0]],
                                   providers[1]:provider_goal[providers[1]],
                                   providers[2]:provider_goal[providers[2]]}
        return top_three_goal_provider


# In[65]:


def top_3_position_goal(Goals):
    goal_position = dict()
    positions = []
    for detail in Goals:
        position = detail['position'].strip()
        if position != '':
            positions.append(position)
        goal_position[position] = goal_position.get(position,0) + 1
    positions = pd.value_counts(positions).keys()
    if(len(positions) < 3):
        return goal_position
    else:
        top_three_goal_position = {positions[0]:goal_position[positions[0]],
                                   positions[1]:goal_position[positions[1]],
                                   positions[2]:goal_position[positions[2]]}
        return top_three_goal_position


# In[66]:


top3_goal_provider(Goals[12]['goal_information']['detail'])


# In[68]:


provider_info = dict()
for g in Goals:
    goals = g['goal_information']['detail']
    if(goals is None):
        continue
    provider = goal_provider(goals)
    for key,value in provider.items():
        if(key != 'null'):
            provider_info[key] = provider.get(key,0) + value


# In[54]:


J = playerGoals()


# In[ ]:


with open('provide_info.json','w') as output:
    json.dump(provider_info,output)


# In[70]:


with open('goal_statis.json','w') as output:
    json.dump(J,output)

