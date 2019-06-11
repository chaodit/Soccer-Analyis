#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json  


# In[18]:


with open('Goal_info_2018.json') as json_data:
    G2018 = json.load(json_data)
    print("***** Goal ***** : " )
    print(json.dumps(G2018[11],indent=4))
with open('Goal_info_2017.json') as json_data:
    G2017 = json.load(json_data)
    print("***** Goal ***** : " )
    #print(json.dumps(Goals[10],indent=4))
with open('Goal_info_2016.json') as json_data:
    G2016 = json.load(json_data)
    print("***** Goal ***** : " )
    #print(json.dumps(Goals[10],indent=4))


# In[22]:


P_2016ID = []
P_2017ID = []
P_2018ID = []

for p in G2016:
    P_ID = p['goal_information']['id']
    P_2016ID.append(P_ID)
for p in G2017:
    P_ID = p['goal_information']['id']
    P_2017ID.append(P_ID)
for p in G2018:
    P_ID = p['goal_information']['id']
    P_2018ID.append(P_ID)   

print(len(P_2016ID))
print(len(P_2017ID))
print(len(P_2018ID))


# In[23]:


oldIn2016 = []

for p in P_2016ID:
    if p not in P_2017ID:
        oldIn2016.append(p)
        P_2017ID.append(p)
print(len(P_2017ID))

for p in G2016:
    if p['goal_information']['id'] in oldIn2016:
        G2017.append(p)
print(len(G2017))


# In[24]:


oldIn2017 = []
for p in P_2017ID:
    if p not in P_2018ID:
        oldIn2017.append(p)
        P_2018ID.append(p)
print(len(P_2018ID))

for p in G2017:
    if p['goal_information']['id'] in oldIn2017:
        G2018.append(p)
print(len(G2018))
#print(json.dumps(G2018[4],indent =4))


# In[25]:


with open('/Users/mac/Dropbox/Soccer/ClubGoalkeeper/goal_details_3s.json','w') as outfile:
    outfile.write('[')
    json.dump(G2018[0],outfile)
    for m in G2018[1:]:
        outfile.write(',\n')
        json.dump(m,outfile)
    outfile.write(']')


# In[ ]:




