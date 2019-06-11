import pandas as pd
import numpy as np
import re
import json
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

# Load the filename from the disk
file_name = ['2015ENG-statistics.json','2015ESP-statistics.json',
            '2015FRA-statistics.json','2015GER-statistics.json',
            '2015ITA-statistics.json','2016ENG-statistics.json',
            '2016ESP-statistics.json','2016FRA-statistics.json',
            '2016GER-statistics.json','2016ITA-statistics.json',
            '2017ENG-statistics.json','2017ESP-statistics.json',
            '2017FRA-statistics.json','2017GER-statistics.json',
             '2017ITA-statistics.json']
# a set of list to store the files data of 3 seasons' data
home_total_shots = []
away_total_shots = []
home_shot_onT = []
away_shot_onT = []
home_shot_offT = []
away_shot_offT = []
home_save = []
away_save = []
home_free_kick = []
away_free_kick = []
home_concer = []
away_concer = []
home_foul = []
away_foul = []
home_offside = []
away_offside = []

#Load the data and store them
for name in file_name:
    file = 'D:\\Text Book\\Project\\Statistics\\' + name
    with open(file,'r') as data:
        mydict = dict()
        mydict = json.load(data)
    for statis in mydict:
        home_total_shots.append(statis['Home Total Shots'])
        away_total_shots.append(statis['Away Total Shots'])
        home_shot_onT.append(statis['Home Shots On Target'])
        away_shot_onT.append(statis['Away Shots On Target'])
        home_shot_offT.append(statis['Home Shots Off Target'])
        away_shot_offT.append(statis['Away Shots Off Target'])
        home_save.append(statis['Home Shots Saved'])
        away_save.append(statis['Away Shots Saved'])
        home_concer.append(statis['Home Corners'])
        away_concer.append(statis['Away Corners'])
        home_free_kick.append(statis['Home Free Kicks'])
        away_free_kick.append(statis['Away Free Kicks'])
        home_foul.append(statis['Home Fouls'])
        away_foul.append(statis['Away Fouls'])
        home_offside.append(statis['Home Offsides'])
        away_offside.append(statis['Away Offsides'])  

def plot_value(list_data):
    # This method plot the whole data of the list
    value = filter_value(list_data)
    value.sort()
    x = np.linspace(0,value[len(value)-1],num=len(value))
    plt.plot(x,value)
    plt.show()
    
def filter_value(list_data):
    # This method filter the null data and convert them to 0
    value = []
    for i in list_data:
        if(i == ' '):
            value.append(0)
        else:
            value.append(int(i))  
    return value

def value_count(value):
    # This method count the occurane of each match data
    count = dict()
    value = filter_value(value) 
    results = list(map(int, value))
    results.sort()
    for i in results:
        count[i] = count.get(i,0) + 1
    return count

def plot_data(count_dic):
    # This method plot the bar chart distribution of the occurance
    plt.xlabel('Times')
    plt.ylabel('Occurance')
    plt.bar(count_dic.keys(),count_dic.values())
    plt.show()

def expection(count_dict):
    # Calculation the expection of each list
    total = sum(list(count_dict.values()))
    exp = 0
    for key,value in count_dict.items():
        exp += key * (value/total)
    return exp

def standar_deviation(count_dict):
    # Calculate tha standard deviation
    data = np.array(list(count_dict.values()))
    return np.std(data,ddof = 1)

def sigmoid(x):
    # sigmod function
    s = 1 / (1 + np.exp(-x))
    return s

def tanh(x):
    # tanh function
    s1 = np.exp(x) - np.exp(-x)
    s2 = np.exp(x) + np.exp(-x)
    s = s1 / s2
    return s

# Plot shot distribution of home shots
home_shots_count = value_count(home_total_shots)
plot_data(home_shots_count)
plot_value(home_total_shots)
# Plot shot distribution of away shots
away_shot_count = value_count(away_total_shots)
plot_data(away_shot_count)
plot_value(away_total_shots)
# Plot shot distribution of home shots on Target
home_onT_count = value_count(home_shot_onT)
plot_data(home_onT_count)
plot_value(home_shot_onT)
# Plot shot distribution of away shots on Target
away_onT_count = value_count(away_shot_onT)
plot_data(away_onT_count)
plot_value(away_shot_onT)
# Plot distribution of home saves
home_save_count = value_count(home_save)
plot_data(home_save_count)
plot_value(home_save)
# Plot distribution of away saves
away_save_count = value_count(away_save)
plot_data(away_save_count)
plot_value(away_save)
# Plot distributon of home freekicks
home_free_kick_count = value_count(home_free_kick)
plot_data(home_free_kick_count)
plot_value(home_free_kick)
# Plot distribution of away freekicks
away_free_kick_count = value_count(away_free_kick)
plot_data(away_free_kick_count)
plot_value(away_free_kick)
# Home corners
home_concer_count = value_count(home_concer)
plot_data(home_concer_count)
plot_value(home_concer)
#Away corners
away_concer_count = value_count(away_concer)
plot_data(away_concer_count)
plot_value(away_concer)
# Home fouls
home_foul_count = value_count(home_foul)
plot_data(home_foul_count)
plot_value(home_foul)
#Away fouls
away_foul_count = value_count(away_foul)
plot_data(away_foul_count)
plot_value(away_foul)

# Out put the performance file
file_name_2 = ['2015ENG-detail.json','2015ESP-detail.json',
            '2015FRA-detail.json','2015GER-detail.json',
            '2015ITA-detail.json','2016ENG-detail.json',
            '2016ESP-detail.json','2016FRA-detail.json',
            '2016GER-detail.json','2016ITA-detail.json',
            '2017ENG-detail.json','2017ESP-detail.json',
            '2017FRA-detail.json','2017GER-detail.json',
             '2017ITA-detail.json']
# a set of list to store the goal information in each match
home_goal = []
away_goal = []
goal_div = []
# read the goal information in each match
for name in file_name_2:
    file = 'D:\\Text Book\\Project\\match_json_v2\\' + name
    with open(file,'r') as data:
        mydict = dict()
        mydict = json.load(data)
    for statis in mydict:
        result = statis['Result'].split(':')
        home_goal.append(int(result[0]))
        away_goal.append(int(result[1]))
        goal_div.append(int(result[0]) - int(result[1]))
    
# Home goals
home_goal_count = value_count(home_goal)
plot_data(home_goal_count)
plot_value(home_goal)
#Away goals
away_goal_count = value_count(away_goal)
plot_data(away_goal_count)
plot_value(away_goal)
# Goal divisions
goal_div_count = value_count(goal_div)
plot_data(goal_div_count)
plot_value(goal_div)

def home_perform_score(total_shots, shots_onT,save,
                       free_kick, conor, foul,
                       goal,goal_div):
    #Performance of home
    #The number is calculate by the central of the distribution
    # Expection of one match is 4/3
    shots_score = sigmoid(total_shots - 10)
    target_score = tanh(shots_onT / 8)
    save_score = tanh(save / 4)
    free_kick_score = sigmoid(free_kick - 14)
    conor_score = tanh(conor / 10)
    foul_score = -sigmoid(foul - 13)
    goal_score = tanh(goal/2)
    div_score = (4/3) * tanh(goal_div)
    performance = (shots_score+target_score+save_score+free_kick_score+conor_score+foul_score+goal_score+div_score) / (5+4/3)
    return performance

def away_perform_score(total_shots, shots_onT,save,
                       free_kick, conor, foul,
                       goal,goal_div):
    #Performance of away
    shots_score = sigmoid(total_shots - 7)
    target_score = tanh(shots_onT / 6)
    save_score = tanh(save / 6)
    free_kick_score = sigmoid(free_kick - 14)
    conor_score = tanh(conor / 6)
    foul_score = -sigmoid(foul - 12)
    goal_score = tanh(goal/2)
    div_score = (4/3) * tanh(goal_div)
    performance = (shots_score+target_score+save_score+free_kick_score+conor_score+foul_score+goal_score+div_score) / (5+4/3)
    return performance

# a list to store the match with match statis, a combination of two files
match_info = []
for i in range(len(file_name)):
    file1 = 'D:\\Text Book\\Project\\Statistics\\' + file_name[i]
    file2 = 'D:\\Text Book\\Project\\match_json_v3\\' + file_name_2[i]
    with open(file1) as f1, open(file2) as f2:
        mydict1 = dict()
        mydict1 = json.load(f1)
        mydict2 = dict()
        mydict2 = json.load(f2)
        for statis1 in mydict1:
            if(statis1['Home Shots On Target'] == ' '):
                continue
            match = dict()
            for stat2 in mydict2:
                if(statis1['Home']['Team ID'] == stat2['Home']['Team ID'] and
                   statis1['Away']['Team ID'] == stat2['Away']['Team ID'] and
                   statis1['Date'] == stat2['Date']):
                    match['Statistics URL'] = statis1['Statistics URL']
                    match['Date'] = statis1['Date']
                    match['Home'] = statis1['Home']
                    match['Away'] = statis1['Away']
                    match['Home Total Shots'] = statis1['Home Total Shots']
                    match['Away Total Shots'] = statis1['Away Total Shots']
                    match['Home Shots On Target'] = statis1['Home Shots On Target']
                    match['Away Shots On Target'] = statis1['Away Shots On Target']
                    match['Home Shots Off Target'] = statis1['Home Shots Off Target']
                    match['Away Shots Off Target'] = statis1['Away Shots Off Target']
                    match['Home Shots Saved'] = statis1['Home Shots Saved']
                    match['Away Shots Saved'] = statis1['Away Shots Saved']
                    match['Home Corners'] = statis1['Home Corners']
                    match['Away Corners'] = statis1['Away Corners']
                    match['Home Free Kicks'] = statis1['Home Free Kicks']
                    match['Away Free Kicks'] = statis1['Away Free Kicks']
                    match['Home Fouls'] = statis1['Home Fouls']
                    match['Away Fouls'] = statis1['Away Fouls']
                    match['Home Offsides'] = statis1['Home Offsides']
                    match['Away Offsides'] = statis1['Away Offsides']
                    match['Home Starters'] = stat2['Home Starters']
                    match['Home Substitutes'] = stat2['Home Substitutes']
                    match['Home Manager'] = stat2['Home Manager']
                    match['Away Starters'] = stat2['Away Starters']
                    match['Away Substitutes'] = stat2['Away Substitutes']
                    match['Away Manager'] = stat2['Away Manager']
                    match['Goals'] = stat2['Goals']
                    result = stat2['Result'].split(':')
                    match['Home Goal'] = int(result[0])
                    match['Away Goal'] = int(result[1])
                    match['Home Goal Div'] = int(result[0]) - int(result[1])
                    match['Away Goal Div'] = int(result[1]) - int(result[0])
                    match_info.append(match)
                    mydict2.remove(stat2)
                    continue           

# Output the combination of match, statistics and performances
match_per = dict()
with open('match_performance.json','w') as outfile:
    for statis in match_info:
        match_per['Statistics URL'] = statis['Statistics URL']
        match_per['Match_id'] = re.findall(r'.*/([0-9]+)',statis['Statistics URL'])[0]
        match_per['Date'] = statis['Date']
        match_per['Home'] = statis['Home']
        match_per['Away'] = statis['Away']
        match_per['Home Goal'] = statis['Home Goal']
        match_per['Away Goal'] = statis['Away Goal']
        match_per['Home Starters'] = statis['Home Starters']
        match_per['Home Substitutes'] = statis['Home Substitutes']
        match_per['Home Manager'] = statis['Home Manager']
        match_per['Away Starters'] = statis['Away Starters']
        match_per['Away Substitutes'] = statis['Away Substitutes']
        match_per['Away Manager'] = statis['Away Manager']
        match_per['Goals'] = statis['Goals']
        match_per['Home_performance'] = str(home_perform_score(int(statis['Home Total Shots']),
                                                               int(statis['Home Shots On Target']),
                                                               int(statis['Home Shots Saved']),
                                                               int(statis['Home Corners']),
                                                               int(statis['Home Free Kicks']),
                                                               int(statis['Home Fouls']),
                                                               statis['Home Goal'],
                                                               statis['Home Goal Div']))                                                        
        match_per['Away_performance'] = str(away_perform_score(int(statis['Away Total Shots']),
                                                           int(statis['Away Shots On Target']),
                                                           int(statis['Away Shots Saved']),
                                                           int(statis['Away Corners']),
                                                           int(statis['Away Free Kicks']),
                                                           int(statis['Away Fouls']),
                                                               statis['Away Goal'],
                                                               statis['Away Goal Div']))
        
        json.dump(match_per,outfile)
        outfile.write(',')
        outfile.write('\n')

