import copy
import datetime
import json
import socket
import time
import urllib.request

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView
from django.db.models import Q

from dateutil import parser

from .fb_info import APP_KEY, APP_SECRET
from .models import Event
from activities.models import Activity
from .forms import EventSearchForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

socket.setdefaulttimeout(30)

# Capture data from FB events JSON file
def capture_data(json_data, page_id):
    real_data = json_data['data'] # type = list that consists of dictionary items
    temp_dictio = {}
    final_list = []
    event_id = ''
    t = (2000, 1, 1, 12, 0, 0, 0, 0, 0)
    t = time.mktime(t)
    converted_time = time.strftime("%m %d %Y %H:%M:%S", time.gmtime(t))
    for dictionary_data in real_data:
        if 'id' in dictionary_data.keys():
            event_id = str(dictionary_data['id'])
        else:
            event_id = ''
        
        if 'owner' in dictionary_data.keys():
            owner = dictionary_data['owner']
            if 'name' in owner.keys():
                temp_dictio['organizer']=owner['name']
            else:
                temp_dictio['organizer']=''
        else:
            temp_dictio['organizer']=''
        
        if 'description' in dictionary_data.keys():
            temp_dictio['description']=dictionary_data['description']
        else:
            temp_dictio['description']=''
            
        if 'start_time' in dictionary_data.keys():
            temp_dictio['start_time'] = parser.parse(dictionary_data['start_time'])
            
        else:
            temp_dictio['start_time']=parser.parse(converted_time)
        
        if 'end_time' in dictionary_data.keys():
            temp_dictio['end_time']=dictionary_data['end_time']
        else:
            temp_dictio['end_time']=parser.parse(converted_time)
        
        if 'place' in dictionary_data.keys():
            place = dictionary_data['place'] # place = dictionary
            
            if 'name' in place.keys():
                temp_dictio['building']=place['name']
            else:
                temp_dictio['building']=''

            if 'location' in place.keys():
                location = place['location']
                if 'city' in location.keys():
                    temp_dictio['city']=location['city']
                else:
                    temp_dictio['city']=''
                if 'zip' in location.keys():
                    temp_dictio['postcode']=location['zip']
                else:
                    temp_dictio['postcode']=''
            else:
                location_key = ['city', 'postcode']
                for key in location_key:
                    temp_dictio[key] = ''
        else:
            place_key = ['building', 'city', 'postcode']
            for key in place_key:
                temp_dictio[key] = ''
        final_list.append(temp_dictio)
        
        # Filter based on event_ID and pageID; If event doesn't exist, create the event. Otherwise, do nothing.
        try:
            event = Event.objects.get(event_id=event_id, page_id=page_id)
        except Event.DoesNotExist:
            event = Event(description=temp_dictio['description'], organizer=temp_dictio['organizer'], building=temp_dictio['building'],city=temp_dictio['city'],postcode=temp_dictio['postcode'], start_time=temp_dictio['start_time'], end_time=temp_dictio['start_time'], event_id=event_id, page_id=page_id)
            event.save()
        temp_dictio={}
    return final_list

def url_retry(url):
    succ = 0
    while succ == 0:
        try:
            json_out = json.loads(urllib.request.urlopen(url).read().decode(encoding="utf-8"))
            succ = 1
        except Exception as e:
#            print(str(e))
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
    final_list = capture_data(next_item, fb_ids)
    
    return final_list

def login(request):
    return render(request, 'login2.html')

def events(request):
    # !------------- DELETE THIS LATER ---------------------------
#    Event.objects.all().delete()
    # !------------- DELETE THIS LATER ---------------------------
    
    scrape_fb(APP_KEY,APP_SECRET, ids="brimbankyouthservices", scrape_mode="events")
    scrape_fb(APP_KEY,APP_SECRET, ids="likeCMY", scrape_mode="events")
    scrape_fb(APP_KEY,APP_SECRET, ids="cnn", scrape_mode="events")
    
    event_list = Event.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 5)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1) # fallback to the first page
    except EmptyPage:
        # probably the user tried to add a page number in the url, so we fallback to the last page
        events = paginator.page(paginator.num_pages)
    
    return render(request, 'events.html', {'events': events})

def search_logic(request, keywords):
    events = Event.objects.filter(
    Q(city__istartswith=keywords) | Q(city__iendswith=keywords) | Q(city__icontains=keywords)
    )
    return events

# Alternative: using SearchQuery & SearchVector
#    events = Event.objects.all()
#    query = SearchQuery(keywords)
#    vector = SearchVector('city')
#    events = events.annotate(search=vector).filter(search=query)
#    events = events.annotate(rank=SearchRank(vector, query)).order_by('-rank')
#    return events
    
def search_from_here(request):
    events = []
    if request.method == 'POST':
        form = EventSearchForm(request.POST)
        if form.is_valid():
            keywords=form.cleaned_data.get('city')
            events = search_logic(request, keywords)
            return render(request, 'event_search2.html', {'events': events, 'form': form})
        else:
            return redirect('error')
    else:
        form = EventSearchForm()
        return render(request, 'event_search2.html', {'events': events, 'form': form})
    
def error(request):
    return render(request, 'error.html')