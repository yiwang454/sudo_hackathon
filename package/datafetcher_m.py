"""This module provides functionality for retrieving real-time and
latest time history level data

"""

import os
import json
import requests

import dateutil.parser
import datetime


def fetch(url):
    """Fetch data from url and return fetched JSON object"""
    myToken = '5d1c9cbab2c13977a828535be6a868fd60882450'
    #myUrl = "https://met.kisanhub.com/api/v2.0/station/"
    head = {'Authorization': 'token {}'.format(myToken)}
    response = requests.get(url, headers=head)
    results = response.text

    data = json.loads(results)
    return data


def dump(data, filename):
    """Save JSON object to file"""
    f = open(filename, 'w')
    data = json.dump(data, f)
    f.close()


def load(filename):
    """Load JSON object from file"""
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    return data


def fetch_station_list(use_cache=True):
    """Fetch data from Environment agency for all active river level
    monitoring stations via a REST API and return retrieved data as a
    JSON object.

    Fetched data is dumped to a cache file so on subsequent call it
    can optionally be retrieved from the cache file. This is faster
    than retrieval over the Internet and avoids excessive calls to the
    Environment Agency service.

    """

    # URL for retrieving data for active stations with river level
    # monitoring (see
    # http://environment.data.gov.uk/flood-monitoring/doc/reference)
    url = "https://met.kisanhub.com/api/v2.0/station/"

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except:
        pass
    cache_file = os.path.join(sub_dir, 'station_data.json')

    # Attempt to load station data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except:
            # If load from file fails, fetch and dump to file
            data = fetch(url)
            dump(data, cache_file)
    else:
        # Fetch and dump to file
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_station(url, start_date, end_date, gateway_slug):
	'''
	This function is calling an API that returns weather information that is recorded by stations
	'''
    myToken = '5d1c9cbab2c13977a828535be6a868fd60882450'
    #myUrl = "https://met.kisanhub.com/api/v2.0/station/"
    head = {'Authorization': 'token {}'.format(myToken)}
    querystring = {"start_date":start_date,"end_date":end_date,"gateway_slug":gateway_slug}
    response = requests.get(url, headers=head, params=querystring)
    
    results = response.text
    data = json.loads(results)
    
    return data
    
def fetch_data_of_the_station(start_date, end_date, gateway_slug, use_cache=True):
    data_list = []
    """Fetch latest levels from all 'measures'. Returns JSON object"""
    page_number = 1
    # URL for retrieving data
    for page_number in range (1,11):
        url =  'https://met.kisanhub.com/api/v2.0/sensor-data/?end_date=%s&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&gateway_slug=6994e966-7598-404b-980b-e2a6b7eb737b&page=%d&start_date=%s'%(end_date,page_number,start_date)
        
        sub_dir = 'cache'
        try:
            os.makedirs(sub_dir)
        except:
            pass
        cache_file = os.path.join(sub_dir, 'level_data.json')
    
        # Attempt to load level data from file, otherwise fetch over
        # Internet
        if use_cache:
            try:
                # Attempt to load from file
                data = load(cache_file)
            except:
                data = fetch_station(url, start_date, end_date, gateway_slug)
                dump(data, cache_file)
        else:
            data = fetch_station(url, start_date, end_date, gateway_slug)
            dump(data, cache_file)
        data_list += data["data"]
    
    return data_list
