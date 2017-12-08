import datetime
import json
import socket
import time
import urllib.request

socket.setdefaulttimeout(30)

# Capture data from FB events JSON file
def capture_data(json_data):
    real_data = json_data['data'] # type = list that consists of dictionary items
    temp_dictio = {}
    final_list = []
    for dictionary_data in real_data:
        temp_dictio['start_time']=dictionary_data['start_time']
        if 'end_time' in dictionary_data.keys():
            temp_dictio['end_time']=dictionary_data['end_time']
        else:
            temp_dictio['end_time']=''
        if 'place' in dictionary_data.keys():
            place = dictionary_data['place'] # place = dict
            temp_dictio['building']=place['name']
            if 'location' in place.keys():
                location = place['location']
                temp_dictio['city']=location['city']
#                print(temp_dictio['city'])
                temp_dictio['country']=location['country']
                temp_dictio['state']=location['state']
                temp_dictio['postcode']=location['zip']
            else:
                temp_dictio['city']=''
                temp_dictio['country']=''
                temp_dictio['state']=''
                temp_dictio['postcode']=''
        final_list.append(temp_dictio)
        temp_dictio={}
    return final_list

def url_retry(url):
    succ = 0
    while succ == 0:
        try:
            json_out = json.loads(urllib.request.urlopen(url).read().decode(encoding="utf-8"))
            succ = 1
        except Exception as e:
            print(str(e))
            if 'HTTP Error 4' in str(e):
                return False
            else:
                time.sleep(1)
    return json_out


def optional_field(dict_item,dict_key):
    try:
        out = dict_item[dict_key]
        if dict_key == 'shares':
            out = dict_item[dict_key]['count']
        if dict_key == 'likes':
            out = dict_item[dict_key]['summary']['total_count']
    except KeyError:
        out = ''
    return out

def scrape_fb(client_id="",client_secret="",token="",ids="",outfile="fb_data.csv",version="2.7",scrape_mode="events",end_date=""):
    time1 = time.time()
    if type(client_id) is int:
        client_id = str(client_id)
    if token == "":
        fb_urlobj = urllib.request.urlopen('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret)
        fb_token = 'access_token=' + json.loads(fb_urlobj.read().decode(encoding="latin1"))['access_token']
    else:
        fb_token = 'access_token=' + token
    if "," in ids:
        fb_ids = [i.strip() for i in ids.split(",")]
    elif '.csv' in ids or '.txt' in ids:
        fb_ids = [i[0].strip() for i in load_data(ids)]
    else:
        fb_ids = [ids]
        
    try:
        end_dateobj = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    except ValueError:
        end_dateobj = ''
        
    for x,fid in enumerate(fb_ids):
        field_list = 'id,description,owner,start_time,end_time,place'
        
    data_url = 'https://graph.facebook.com/v' + version + '/' + fid.strip() + '/' + scrape_mode + '?fields=' + field_list + '&limit=100&' + fb_token
    
    next_item = url_retry(data_url)
    final_list = capture_data(next_item)

    return final_list
    