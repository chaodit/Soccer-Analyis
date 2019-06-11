#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import re


# In[18]:


with open('manager_info_2016.json', 'r') as json_data:
    M2016 = json.load(json_data)
    print ("***** M2016 ***** : ")
    #print (json.dumps(M2016[0], indent=4))  
with open('manager_info_2017.json') as json_data:
    M2017 = json.load(json_data)
    print("***** M2017 ***** : " )
    #print(json.dumps(M2017[0], indent=4))
with open('manager_info_2018.json') as json_data:
    M2018 = json.load(json_data)
    print("***** M2018 ***** : " )
    #print(json.dumps(M2018[0], indent=4))


# In[19]:


with open('Player_2016.json') as json_data:
    P2016 = json.load(json_data)
    print("***** P2016 ***** : " )
    #print(json.dumps(P2016[10], indent=4))
with open('Player_2017.json') as json_data:
    P2017 = json.load(json_data)
    print("***** P2017 ***** : " )
    #print(json.dumps(P2017[10], indent=4))
with open('Player_2018.json') as json_data:
    P2018 = json.load(json_data)
    print("***** P2018 ***** : " )
    #print(json.dumps(P2018[10], indent=4))


# In[5]:


with open('club_info_2016.json') as json_data:
    C2016 = json.load(json_data)
    print("***** C2016 ***** : " )
with open('club_info_2017.json') as json_data:
    C2017 = json.load(json_data)
    print("***** C2017 ***** : " )
with open('club_info_2018.json') as json_data:
    C2018 = json.load(json_data)
    print("***** C2018 ***** : " )
    #print(json.dumps(C2018[10], indent=4))


# In[6]:


with open('Playerperform_2016.json') as json_data:
    PF2016 = json.load(json_data)
    print("***** PF2016 ***** : " )
with open('Playerperform_2017.json') as json_data:
    PF2017 = json.load(json_data)
    print("***** PF2017 ***** : " )
with open('Playerperform_2018.json') as json_data:
    PF2018 = json.load(json_data)
    print("***** PF2018 ***** : " )
    #print(json.dumps(PF2018, indent=4))


# In[7]:


M_2016ID = []
M_2017ID = []
M_2018ID = []

for m in M2016:
    M_ID = m['manager_detail']['id']
    M_2016ID.append(M_ID)
for m in M2017:
    M_ID = m['manager_detail']['id']
    M_2017ID.append(M_ID)
for m in M2018:
    M_ID = m['manager_detail']['id']
    M_2018ID.append(M_ID)   

print(len(M_2016ID))
print(len(M_2017ID))
print(len(M_2018ID))


# In[8]:


oldIn2016 = []
for m in M_2016ID:
    if m not in M_2017ID:
        oldIn2016.append(m)
        M_2017ID.append(m)
print(len(M_2017ID))

for m in M2016:
    if m['manager_detail']['id'] in oldIn2016:
        #print(m['manager_detail']['id'])
        #print(m)
        M2017.append(m)
print(len(M2017))


# In[9]:


oldIn2017 = []
for m in M_2017ID:
    if m not in M_2018ID:
        oldIn2017.append(m)
        M_2018ID.append(m)
print(len(M_2018ID))

for m in M2017:
    if m['manager_detail']['id'] in oldIn2017:
        #print(m['manager_detail']['id'])
        #print(m)
        M2018.append(m)

print(len(M2018))


# In[20]:


P_2016ID = []
P_2017ID = []
P_2018ID = []

for p in P2016:
    P_ID = p['player_detail']['id']
    P_2016ID.append(P_ID)
for p in P2017:
    P_ID = p['player_detail']['id']
    P_2017ID.append(P_ID)
for p in P2018:
    P_ID = p['player_detail']['id']
    P_2018ID.append(P_ID)   

print(len(P_2016ID))
print(len(P_2017ID))
print(len(P_2018ID))


# In[24]:


oldIn2016 = []
for p in P_2016ID:
    if p not in P_2017ID:
        oldIn2016.append(p)
        P_2017ID.append(p)

print(len(P_2017ID))

for p in P2016:
    if p['player_detail']['id'] in oldIn2016:
        #print(m['manager_detail']['id'])
        #print(m)
        P2017.append(p)
print(len(P2017))


# In[12]:


oldIn2017 = []
for p in P_2017ID:
    if p not in P_2018ID:
        oldIn2017.append(p)
        P_2018ID.append(p)
print(len(P_2018ID))

for p in P2017:
    if p['player_detail']['id'] in oldIn2017:
        #print(m['manager_detail']['id'])
        #print(m)
        P2018.append(p)


# In[13]:


Players = []
for p in P2018:
    jsonObj = {
        "player_detail": {
            "name": p['player_detail']['name'],
            "id": p['player_detail']['id'],
            "url": p['player_detail']['url'],
            "detail": {
                "dob": p['player_detail']['detail']['dob'],
                "height": p['player_detail']['detail']['height'],
                "citizenship": p['player_detail']['detail']['citizenship'],
                "agent":  p['player_detail']['detail']['agent']},
            "perform":[]
        }
    }
    Players.append(jsonObj)


# In[14]:


#2016
for p in Players:
    performObj = {
        "season": "15/16", 
        "position": None,
        "club_name": None,
        "club_id": None,
        "market_value": None,
        "detail": []}
    for pf in PF2016:
        if p['player_detail']['id'] == pf['player_perform']['id']:
            performObj['detail'].append(pf['player_perform']['detail'])
            break
    for pc in C2016:
        for pc2 in pc['club_information']['detail']:
            if p['player_detail']['id'] == pc2['id']:
                performObj['position'] = pc2['position']
                performObj['market_value'] = pc2['market value']
                performObj['club_name'] = pc['club_information']['name']
                performObj['club_id'] = pc['club_information']['id']
                break
    if (performObj['position'] != None) or (len(performObj['detail'])) != 0:
        #print(performObj)
        p['player_detail']['perform'].append(performObj)
          


# In[15]:


#2017
for p in Players:
    performObj = {
        "season": "16/17", 
        "position": None,
        "club_name": None,
        "club_id": None,
        "market_value": None,
        "detail": []}
    for pf in PF2017:
        if p['player_detail']['id'] == pf['player_perform']['id']:
            performObj['detail'].append(pf['player_perform']['detail'])
            break
    for pc in C2017:
        for pc2 in pc['club_information']['detail']:
            if p['player_detail']['id'] == pc2['id']:
                performObj['position'] = pc2['position']
                performObj['market_value'] = pc2['market value']
                performObj['club_name'] = pc['club_information']['name']
                performObj['club_id'] = pc['club_information']['id']
                break
    if (performObj['position'] != None) or (len(performObj['detail'])) != 0:
        #print(performObj)
        p['player_detail']['perform'].append(performObj)


# In[16]:


#2018
for p in Players:
    performObj = {
        "season": "17/18", 
        "position": None,
        "club_name": None,
        "club_id": None,
        "market_value": None,
        "detail": []}
    for pf in PF2018:
        if p['player_detail']['id'] == pf['player_perform']['id']:
            performObj['detail'].append(pf['player_perform']['detail'])
            break
    for pc in C2018:
        for pc2 in pc['club_information']['detail']:
            if p['player_detail']['id'] == pc2['id']:
                performObj['position'] = pc2['position']
                performObj['market_value'] = pc2['market value']
                performObj['club_name'] = pc['club_information']['name']
                performObj['club_id'] = pc['club_information']['id']
                break
    if (performObj['position'] != None) or (len(performObj['detail'])) != 0:
        #print(performObj)
        p['player_detail']['perform'].append(performObj)


# In[24]:


goal_JsonArray = []

for g in Goals:
    if g['goal_information']['detail'] != None:
        jsonObje = {
           "goal_information": {
                "name": g['goal_information']['name'],
                "id": g['goal_information']['id'],
                "url": g['goal_information']['url'],
                "detail":[]
           }
        }
        for d in g['goal_information']['detail']:
            if d['season'] == "15/16" or d['season'] == "16/17" or d['season'] == "17/18":
                print(d)
                jsonObje['goal_information']['detail'].append(d)
        goal_JsonArray.append(jsonObje)


# In[18]:


with open('/Users/mac/Dropbox/Soccer/Analysis/manager_all.json','w') as outfile:
    outfile.write('[')
    json.dump(M2018[0],outfile)
    for m in M2018[1:]:
        outfile.write(',\n')
        json.dump(m,outfile)
    outfile.write(']')


# In[19]:


with open('/Users/mac/Dropbox/Soccer/ENG_player_all.json','w') as outfile:
    outfile.write('[')
    json.dump(Players[0],outfile)
    for m in Players[1:]:
        outfile.write(',\n')
        json.dump(m,outfile)
    outfile.write(']')

