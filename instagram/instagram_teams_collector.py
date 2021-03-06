# -*- coding: utf-8 -*-
"""
@author: ASUS
"""

import pandas as pd
from instagram_search import search_team
from django.utils.encoding import smart_str

teams = pd.read_csv("teams.csv")
team_list = teams['team_name']

header = "team_name,insta_name,ista_id,media_count,followed_by,follows,website\n"
text = open("teams_insta.csv", "a")
text.write(header)
text.close()
for num in range(0,len(team_list)):
    team = team_list[num]
    
    team_tup = search_team(team)
    
    line = team
    for i in team_tup:
        line += "," + smart_str(i)
    line += "\n"
    line = line.replace('"',"")
    print line
    line = smart_str(line)
    text = open("teams_insta.csv", "a")
    text.write(line)
    text.close()