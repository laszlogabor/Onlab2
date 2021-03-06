# -*- coding: utf-8 -*-
"""
@author: ASUS
"""

import instagram
#from instagram import InstagramAPI
from spec_char_remover import remove_spec

def set_api():
    client_id = "fb0a9594fbe14e72990c716c33b3f1d7"
    client_secret = "c79a43ed0e8441c2a0ff7b2cc11b9e4a"
    access_token = "2263070228.e029fea.1c3fc5838aea4f5685f9a5964ed36e7e"
    api = instagram.client.InstagramAPI(client_id=client_id, client_secret=client_secret, access_token=access_token)
    return api

def instagram_search_team(query):
    api = set_api()
    user_name = remove_spec(query)
    try:
        search_result = api.user_search(q=user_name)
        page_list = []
        for i in range(len(search_result)):
            try:
                user = api.user(search_result[i].id)
#                print (user.counts['followed_by'])
                page_tuple = (user, user.counts['followed_by'])
                page_list.append(page_tuple)
            except:
                None

        user = max(page_list,key=lambda item:item[1])[0]
        
#        user = api.user(search_result[0].id)
        page_dict = {'instagram_name' : user.username,
                     'instagram_id': user.id,
                     'instagram_media': user.counts['media'],
                     'instagram_followers': user.counts['followed_by'],
                     'instagram_follows' : user.counts['follows'],
                     'instagram_url' : user.website}
        return page_dict

    except:
        page_dict = {'instagram_name' : "NaN",
                     'instagram_id': "NaN",
                     'instagram_media': "NaN",
                     'instagram_followers': "NaN",
                     'instagram_follows' : "NaN",
                     'instagram_url' : "NaN"}
        return page_dict
