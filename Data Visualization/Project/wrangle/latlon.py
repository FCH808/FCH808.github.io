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
import pandas as pd


def lookup_lat_lon(location_string):
    """ Returns an http request string to Google maps api.
    
    Args:
        location_string: String with location to look up.
    Returns:
        A string of the http request link to the city/state/country passed in.
    """
    google_api_key = "AIzaSyDAJxRxTE-ZC5M7qGN5Bg_FXwgc5e_TqdU"    
    

    base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    
    return base + location_string + "&key=" + google_api_key

def find_lon_lat(location):
    '''Returns city, country, country short name, longitude and latitude
        of given city/state/country.
        
    Args:
        Location string of city/state/country
    Returns:
        Six strings: location, city_name, country_long_name, 
                      country_short_name, lon, lat
    '''
    
    # https://console.developers.google.com
    # https://developers.google.com/maps/documentation/geocoding/?csw=1    
    city_name = ""
    country_long_name = ""
    country_short_name = ""
    lon = ""
    lat = ""
    
    url = lookup_lat_lon(location)
    r = requests.get(url)
    country_json = r.json()
    try:
        # Google does a good job of ranking the best result first. Use first
        # result.
        lat = country_json['results'][0]['geometry']['location']['lat']
        lon = country_json['results'][0]['geometry']['location']['lng']
        # Check for the country-political for correct country abbreviation.
        for first_result in country_json['results'][0]['address_components']:
                if first_result['types'] == ['country', 'political']:
                    country_short_name = first_result['short_name']
                    country_long_name = first_result['long_name']


    except IndexError as e:
        print "*"*80
        print "COUNTRY_JSON: ", country_json
        print "LOCATION: ", location
        print "URL: ", url
        print "ERROR: ", e
        city_name = location
        country_long_name = e
        country_short_name = e
        lon = e
        lat = e
        return location, city_name, country_long_name, country_short_name, lon, lat
    
    return location, city_name, country_long_name, country_short_name, lon, lat
    
def find_lon_lat_to_df(city_lookups):
    '''Looks up lon/lat for cities in list of cities and returns dataframe.
    
    Args:
        city_lookups: list of cities as strings to look up
    Returns:
        Pandas dataframe of location, city, country, country_short_name,
            lon, lat of a given city
    '''
    header = ['location', 'city_name', 'country',
              'country_short_name', 'lon', 'lat']
    
    all_cty_info = []
    
    for city in city_lookups:
        # Package output into a list..
        location, city_name, country_long_name, country_short_name, lon, lat =\
        find_lon_lat(city)
        # ... and  append to list of cities
        all_cty_info.append( [location, city_name, country_long_name,
                              country_short_name, lon, lat] )
        
    df = pd.DataFrame(all_cty_info, columns=header)
    return df