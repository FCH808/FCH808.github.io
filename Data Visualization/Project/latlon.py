# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:56:47 2015
@author: fch

Library for returning geo-coordinates (latitude, longitude) from various 
    inputs.

Available functions:
 - lookup_lat_lon: 

"""
import requests


def lookup_lat_lon(country="", city="", state="", key=""):
    """ Returns an http request string to Google maps api.
    
    Args:
        city: string - City to look up.
        state: string - State to look up.
        country: string - Country to lookup.
        key: string - Google maps api keys.
    Returns:
        A string of the http request link to the city/state/country passed in.
    
    """
    location = ""
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    if city != "":
        location += city
    if state != "":
        location += "+" + state
    if country != "":
        location += "+" + country
    return base+"address="+location+"&key="+key
    
def get_long_lat(location_list, country_type=None):
    
    assert country_type.lower() == 'birth' or country_type.lower() == "acquired", \
        "Please enter 'birth' for birth countries, or 'acquired' for country\
 Nobel Prize was acquired in."
    

    if country_type.lower() == 'acquired':
        output = [['acquired_lat', 
                   'acquired_lon', 
                   'current_country_name_acquired',
                   'acquired_country_short_name',
                   'city',
                   'state']]
                   
    elif country_type.lower() == 'birth':
        output = [['birth_lat', 
                   'birth_lon', 
                   'birth_country_current_name',
                   'birth_country_short_name',
                   'city',
                   'state']]        
        
    # https://console.developers.google.com
    # https://developers.google.com/maps/documentation/geocoding/?csw=1
    google_api_key = "AIzaSyDAJxRxTE-ZC5M7qGN5Bg_FXwgc5e_TqdU"
    

    for each_country in location_list:

        country, city, state = each_country.split("_SEP_")
        url = lookup_lat_lon(country, city, state, key=google_api_key)
        r = requests.get(url)
        country_json = r.json()
        try:
            lat = country_json['results'][0]['geometry']['location']['lat']
            lon = country_json['results'][0]['geometry']['location']['lng']
            #country_long_name = country_json['results'][0]['address_components'][0]['long_name']
            country_long_name = country
            for result in country_json['results']:
                for address_component in result['address_components']:
                    if address_component['types'] == ['country', 'political']:
                        # country_long_name = address_component['long_name']
                        country_short_name = address_component['short_name']
        except IndexError as e:
            print "*"*80
            print "COUNTRY_JSON: ", country_json
            print "COUNTRY: ", country
            print "CITY: ", city
            print "STATE: ", state
            print "URL: ", url
            print "ERROR: ", e
            pass
            
        output.append([lat, lon, country_long_name, 
                       country_short_name, city, state])
    
    return output