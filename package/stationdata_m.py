"""This module provides interface for extracting statiob data from
JSON objects fetched from the Internet 

"""

import datafetcher_m
import time, threading
import dateutil.parser
import datetime

class MonitoringStation:
    """This class represents a weather monitoring station"""

    def __init__(self, gateway,latitude,longitude, wind_speed,temperature,
                 dew_point, wind_direction,relative_humidity, precipitation, time, spray = True):

       
        self.latitude = latitude
        self.longitude=longitude
        self.gateway = gateway
        
        self.wind_speed = wind_speed
        self.temperature = temperature
        self.dew_point = dew_point
        self.wind_direction = wind_direction
        self.relative_humidity = relative_humidity
        self.precipitation = precipitation
        self.spray=spray
        self.time = time
        
    def forbid_spray(self):
        self.spray=False

    def __repr__(self):
        
        
        d  = "gateway   :             {}\n".format(self.gateway)
        d += "latitude   :            {}\n".format(self.latitude)
        d += "longitude   :          {}\n".format(self.longitude)
        
        d += "wind_speed   :          {}\n".format(self.wind_speed)
        d += "temperature   :         {}\n".format(self.temperature)
        d += "dew_point   :           {}\n".format(self.dew_point)
        d += "wind_direction   :      {}\n".format(self.wind_direction)
        d += "relative_humidity   :   {}\n".format(self.relative_humidity)
        d += "precipitation   :       {}\n".format(self.precipitation)
        d += "time   :                {}\n".format(self.time)
        
        return d
    
    
    def too_dew(self):
        if self.dew_point>self.temperature:
            self.spray=False

    def get_wind_predict_graph(self):
           #do the thing!
        f = plt.figure()
        f.savefig('the graph.png')
        self.wind_predict_graph='' #get url of the graph

def build_station_list(use_cache=True):
    """Build and return a list of all weather monitoring stations
    based on data fetched from the KisanHub API. Each station with a certain time spot is
    represented as a MonitoringStation object.

    The available data for some station is incomplete or not
    available.

    """

    # Fetch station data
    data = datafetcher_m.fetch_station_list(use_cache)

    # Build list of MonitoringStation objects
    stations = []
    for e in data["data"]:
        
        #print(e['location']['longitude'],)
        # Extract town string (not always available)
        
        
        # Extract river name (not always available)
       
        s = MonitoringStation(gateway=e['nodes'][0]['gateway'],
                                  latitude=e['location']['latitude'],
                                  longitude=e['location']['longitude'],
                                  wind_speed = None,
                                  temperature = None,
                                  dew_point = None
                                  ,wind_direction = None
                                  ,relative_humidity = None,precipitation = None
                                  ,time = None)
        stations.append(s)
        
    return stations

def update_station_period(station, start_date, end_date):
    '''
    This function output a dictionary of measurement of a certain station in a period of time
    key: date_time
    item: a list of measurements of one stations in several time spots in a time period between the start and end dates
    '''
    
    station_all_data = dict()
    A = datafetcher_m.fetch_data_of_the_station(start_date, end_date, station.gateway)
    
    for i in A:
            
        station_all_data[i['date_time']] = i
        
    return station_all_data

date = str(datetime.datetime.now())
end_date = date[0:10]
start_date2 = end_date
day =str(int(end_date[9])-1)
start_date = start_date2.replace(start_date2[9],day)
#print(update_station_period(build_station_list()[0], start_date, end_date))

#print(type()) #for debugging purpose


#print(update_station_period(B[0]))  #for debugging purpose

def update_stations_data(start_date, end_date):
    """
    out put a dictionary of list showing measurements on a series of stations at a certain time spot
    key: string showing the time spot; the keys are series of time spots from a certain time periods
    items： lists showing measurements on a series of stations at the time spot in that key
    """
    stations = build_station_list()
    
    station_data_with_time = dict()
    time_list = []
    for member in update_station_period(stations[0], start_date, end_date):
        time_list.append(member)
    i = 0
    for time_member in time_list:
        
        stations_list = []#list of station objects with same time and different actual stations
    # Attach latest reading to station objects
        i += 1
        if i >= 2:
            break
        
        
        for station in stations:
            
            new_data = update_station_period(station, start_date, end_date) #is a dictionary of dictionary
            
            s = station
            try:
                s.time = time_member
            
                #print(new_data[time_member])
                s.wind_speed = new_data[time_member]['wind_speed']
                s.temperature = new_data[time_member]['temperature']
                s.dew_point = new_data[time_member]['dew_point']
                s.wind_direction = new_data[time_member]['wind_direction']
                s.relative_humidity = new_data[time_member]['relative_humidity']
                s.precipitation = new_data[time_member]['precipitation']
            except:
                pass
                
            stations_list.append(s)
            
        station_data_with_time[time_member] = stations_list

    return station_data_with_time

#print(len(update_stations_data(B)['2018-04-05T00:00:00'])) #for debugging purpose
'''
date = str(datetime.datetime.now())
end_date = date[0:10]
start_date2 = end_date
day =str(int(end_date[9])-1)
start_date = start_date2.replace(start_date2[9],day)


time_stations = update_stations_data(start_date, end_date)
print(time_stations)

'''