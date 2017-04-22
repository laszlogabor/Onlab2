# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 14:21:09 2017

@author: ASUS
"""

import urllib2
import json
import pandas as pd
from django.utils.encoding import smart_str

access_token = "614700401966588|7af8b0fda1b43f908b8853ed65e8b648"  # Access Token

def get_correct_page(page_id):
    api_endpoint = "https://graph.facebook.com/v2.4/"
    fb_graph_url = api_endpoint+page_id+"?fields=id,name,likes,link,talking_about_count,category&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

def facebook_search_team(team):
    team = team.replace(" ","%20")
    search = search_team(team)
    page_list = []
    for i in search['data']:
        page_data = get_correct_page(i['id'])
        page_tup = (page_data['name'], i['id'],  page_data['likes'], page_data['link'], page_data['category'])
#        if page_tup[4] == "Sports Team":
#            page_list.append(page_tup)
        page_list.append(page_tup)

    try:
        official_page = max(page_list,key=lambda item:item[2])
        page_json = get_correct_page(official_page[1])
        page_dict = {'facebook_name' : page_json['name'].replace(",",";"),
                     'facebook_id' : page_json['id'],
                     'facebook_likes' : page_json['likes'],
                     'facebook_talking_about_count' : page_json['talking_about_count'],
                     'facebook_category' : page_json['category'].replace(",",";"),
                     'facebook_url' : page_json['link'].replace(",",";")
                     }
        return page_dict
    except:
        page_dict = {'facebook_name' : "NaN",
                     'facebook_id' : "NaN",
                     'facebook_likes' : "NaN",
                     'facebook_talking_about_count' : "NaN",
                     'facebook_category' : "NaN",
                     'facebook_url' : "NaN"
                     }
        return page_dict
            
def search_team(query):
    fb_graph_url = "https://graph.facebook.com/search?q=" + query + "&type=page&access_token=" + access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

def get_page_fans(query,access_token, start_date, final_date):
    fb_graph_url = "https://graph.facebook.com/v2.6/" + query + "/insights/page_fans_country/lifetime?&since=" + start_date + "&until=" + final_date + "&access_token=" + access_token

    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

def get_name(team):
    return facebook_search_team(team)['facebook_name']
    
def get_id(team):
    return facebook_search_team(team)['facebook_id']
    
def get_link(team):
    return facebook_search_team(team)['facebook_url']

def get_likes(team):
    return facebook_search_team(team)['facebook_likes']

def get_talking_about(team):
    return facebook_search_team(team)['facebook_talking_about_count']   
    
def get_category(team):
    return facebook_search_team(team)['facebook_category']
    
def facebook_generate_csv(team_list):
    output_name = team_list.replace("list","facebook_stats")
    header = "facebook_name,facebook_id,facebook_likes,facebook_talking_about_count,facebook_category,facebook_url\n"
    text = open(output_name, "a")
    text.write(header)
    text.close()
    teams = pd.read_csv(team_list)
    for i in range(len(teams)):
        team = teams.iat[i,0]
        print team
        team_stats = facebook_search_team(team)
        line = ""
#        line = team + ","
#        line = smart_str(line)
        line += team_stats['facebook_name'] + ","
        line += str(team_stats['facebook_id']) + ","
        line += str(team_stats['facebook_likes']) + ","
        line += str(team_stats['facebook_talking_about_count']) + ","
        line += team_stats['facebook_category']
        line += "," + team_stats['facebook_url']
        line += "\n"
        line = smart_str(line)
        print line
        text = open(output_name, "a")
        text.write(line)
        text.close()

def update_likes(input_csv):
    #TODO: regenerate the like 
    None

"""
Some extra links

link = "https://graph.facebook.com/DiamondPlatnumz255?access_token=614700401966588|7af8b0fda1b43f908b8853ed65e8b648"
https://graph.facebook.com/v2.6/204153042939851/posts/?fields=message,link,permalink_url,created_time,type,name,id,comments.limit(0).summary(true),shares,likes.limit(0).summary(true),reactions.limit(0).summary(true)&limit=100&access_token=614700401966588|7af8b0fda1b43f908b8853ed65e8b648
https://graph.facebook.com/search?q=manchester+united&type=page&access_token=614700401966588%7C7af8b0fda1b43f908b8853ed65e8b648
https://graph.facebook.com/v2.6/barackobama/insights/page_fans_country/lifetime?&since=2016-06-01&until=2016-09-02&access_token=614700401966588|7af8b0fda1b43f908b8853ed65e8b648
https://graph.facebook.com/v2.6/7724542745/insights/page_fans_country/lifetime?&since=2016-06-01&until=2016-09-02&access_token=614700401966588|7af8b0fda1b43f908b8853ed65e8b648

"""