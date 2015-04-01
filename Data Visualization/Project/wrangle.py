# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\fch80_000\.spyder2\.temp.py
"""
import pandas as pd
from latlon import *
import re

def find_country_acq(bs4_html):
    """ Parse BeautifulSoup html request object into list of lists of the 
        important information.
    
    Args:
        bs4_html: BeautifulSoup html request object
    Returns:
        List of lists containing [name, institution, old_country_name_acquired,
                                  current_country_name_acquired, city, state, 
                                  year, field] for each entry.
    """
    all_names = [["name", "institution",
                  "old_country_name_acquired","current_country_name_acquired",
                  "city","state","year","field"]]
    place_acq = ""
    for i in bs4_html:
        #pprint.pprint(i) 
        #print "*"*80
        #print i
        ## Acquisition location is buried in h3 headers
        if i.find_all('h3'):
            #print "i.TEXT: ", i.text
            place_acq = i.h3.text
        if i.find_all('a'):
            #print ""
            #print "i.a.TEXT: ", i.a.text
            #print "i.h6.TEXT: ", i.h6.text
            #print "PLACE_ACQ: ", place_acq
            #print "field_year: ", field_year
            ## Other information is in the a div's
            field_year = i.a.text
            name = i.h6.text
            
         
                
            year, field = grab_field_and_number(field_year)
            institution, country, city, state, extra_loc = grab_inst_country_citystate(place_acq)
        

            old_country_name, new_country_name = separate_old_country_names(country)
            
            
            all_names.append([name.encode('utf-8').strip(),
                              institution.encode('utf-8').strip(),
                              old_country_name.encode('utf-8').strip(),
                              new_country_name.encode('utf-8').strip(),
                              city.encode('utf-8').strip(), 
                              state.encode('utf-8').strip(),
                              year.encode('utf-8').strip(),
                              field.encode('utf-8').strip()])
            
            #print ""
            #print "*"*80
    return df_from_lists(all_names, header_included=True)
    
def find_country_birth(bs4_html):
    all_names = [["name","birth_country_old_name",
                  "birth_country_current_name",
                  "year","field"]]
    place_acq = ""
    for i in bs4_html:
        # Only place acquired entries have an 'h3' sub-class
        if i.find_all('h3'):
            place_acq = i.h3.text
        # Only field_year/name entries have an 'h6' sub-class.
        if i.find_all('h6'):
            field_year = i.a.text
            name = i.h6.text
            year, field = grab_field_and_number(field_year)
            old_country_name, new_country_name = separate_old_country_names(place_acq)
            
            all_names.append([name.encode('utf-8').strip(), 
                              old_country_name.encode('utf-8').strip(),
                              new_country_name.encode('utf-8').strip(),
                              year.encode('utf-8').strip(),
                              field.encode('utf-8').strip()])
            
    return df_from_lists(all_names, header_included=True)

def find_age(bs4_html):
    all_names = [["name", "age"]]
    # place_acq = ""
    for i in bs4_html[6].find_all(['h3', 'h6']): 
        if "Age" in i.string:
            age = i.string.split()[-1]
        if "Age" not in i.string:
            name = i.string
            all_names.append([name.encode('utf-8'), age.encode('utf-8')])
    return df_from_lists(all_names, header_included=True) 

def grab_city_state(city_state, country):
    '''
    
    >>> grab_city_state(["Cardio-Pulmonary Laboratory", "Bellevue Hospital", "New York", "NY"])
    ('NY', 'New York', 'Cardio-Pulmonary Laboratory, Bellevue Hospital')
    
    >>> grab_city_state(["Bellevue Hospital", "New York", "NY"])
    ('NY', 'New York', 'Bellevue Hospital')
    
    >>> grab_city_state(['New York', 'NY'])
    ('NY', 'New York', '')
    
    >>> grab_city_state(['New York'])
    ('New York', '', '')
    
    '''
    city = ""
    state = ""    
    other = ""
    if len(city_state) == 1:
        city = city_state.pop()

    elif len(city_state) > 1:
        if country == "USA":
            state = city_state.pop()
            city = city_state.pop()
        else:
            city = city_state.pop()
            # Handle a problem case of ';'  in Altenberg; Grünau im Almtal
            city = city.split(';')[0]
    other = ", ".join(city_state)
    #print "+"*80
    #print "A_CITY: ", city
    #print "A_STATE: ", state
    #print "A_OTHER: ", other
    return city.strip(), state.strip(), other.strip()

def grab_inst_country_citystate(location):
    '''
    
    >>> grab_inst_country_citystate("Edinburgh University, Edinburgh, United Kingdom")
    ('Edinburgh University', 'United Kingdom', 'Edinburgh', '', '')
    
    >>> grab_inst_country_citystate("Fred Hutchinson Cancer Research Center, Seattle, WA, USA")
    ('Fred Hutchinson Cancer Research Center', 'USA', 'WA', 'Seattle', '')
    
    >>> grab_inst_country_citystate("Columbia University Division, Cardio-Pulmonary Laboratory, Bellevue Hospital, New York, NY, USA")
    ('Columbia University Division', 'USA', 'NY', 'New York', 'Cardio-Pulmonary Laboratory,  Bellevue Hospital')
    
    >>> grab_inst_country_citystate('Strasbourg University, Strasbourg, Alsace (then Germany, now France)')
    ('Strasbourg University', 'Alsace (now France)', 'Strasbourg', '', '')


    '''
    # Handle corner case.
    location = location.replace('then Germany, ', '')
    # Handle record with missing data.
    if location == 'Howard Hughes Medical Institute, , ':
        location = 'Howard Hughes Medical Institute, Chevy Chase, MD, USA'    
    
    pieces = location.split(",")
    institution = pieces[0].strip()
    country = pieces[-1].strip()
    city_state = pieces[1:-1]
    #print "*"*80
    #print "LOCATION: ", location
    #print "INSitutiON: ", institution
    #print "CITY/STATE: ", city_state
    #print "COUNTRY: ", country
    city, state, extra_loc = grab_city_state(city_state, country)
    # Fix problem records for Google map api lookup.
    if country == "USSR":
        country = "Russia"
    if country == "Czechoslovakia":
        country = "Czech Republic"
    return institution, country, city, state, extra_loc
    
def separate_old_country_names(country):
    """Return old and new country if applicable.
    
    Given a string with two country names, returns the old and new names.
    
    Args:
        country: string containing country name. May have old and new names.
    Returns:
        string of old country name and string of current country name.
        *If the country name had not changed, returns same name for both*
    
    >>> separate_old_country_names(' Alsace (now France)')
    ('Alsace', 'France')
    
    """
    old = ""
    new = ""
#    if " (now " in country:
#        old_and_new = country.split(' (now ')
    if "now " in country:
        split_string = re.search('\(.*now ', country).group(0)
        old_and_new = country.split(split_string)
        old = old_and_new[0]
        new = old_and_new[1][:-1]
    else:
        old = country
        new = country
    return old.strip(), new.strip()    
 

   
def grab_field_and_number(year_field):
    ''' Parse Nobel Prize year-feild strings into substrings with year and field 
        separated.
        
    Args:
        year_field: String containing Nobel Prize year and field.
    Returns:
        One string containing the year. One string containing the field of the 
            Nobel Prize awarded.
    
    >>> grab_field_and_number("The Nobel Prize in Physics 2000")
    ('2000', 'Physics')
    
    >>> grab_field_and_number("The Prize in Economic Sciences 2010")
    ('2010', 'Economic Sciences')
    
    >> >grab_field_and_number("The Nobel Prize in Physiology or Medicine 2000")
    ('2000', 'Physiology or Medicine')
    
    >>> grab_field_and_number("The Nobel in Peace Prize 2010")
    ('2010', 'Peace')
    '''
    
    if "Economic" in year_field:
        temp_string = year_field.split()
        year = temp_string.pop()
        field = temp_string[-2] + " " + temp_string[-1]
    elif "Physiology or Medicine" in year_field:
        temp_string = year_field.split()
        year = temp_string.pop()
        field = temp_string[-3] + " " + temp_string[-2] + " " + temp_string[-1]
    elif "Peace" in year_field:
        temp_string = year_field.split()
        year = temp_string.pop()
        field = temp_string[-2]
    else:
        temp_string = year_field.split()
        year = temp_string.pop()
        field = temp_string[-1]
    return year, field

def create_lat_lon(df=None, country_type="acquired", country_col="", city_col="", state_col=""):
    """Create latitude and longitude dataframe from Pandas Dataframe with
        location info.
    """
    
    assert country_col != "", "Please enter column that contain country names."
    
    # TODO: refactor default args better
    if city_col != "" and state_col != "":
        locations = list(set(df[country_col] + "_SEP_" + df[city_col] + \
        "_SEP_" + df[state_col]))
    # TODO: Handle any combination. Currently only needs country, or all 3.
    else:
        # Add SEP for splitting into 3 strings later.
        locations = list(set(df[country_col] + "_SEP_" + "_SEP_"))

    lat_lon_list = get_long_lat(locations, country_type=country_type)
    return df_from_lists(lat_lon_list)

def df_from_lists(lists, header_included=True):
    """Makes pandas dataframe from list of lists. 
    """
    # Mutating global copy of list? Make a copy here.
    inside_lists = lists[:]
    headers = None
    if header_included:
        headers = inside_lists.pop(0)

    df = pd.DataFrame(inside_lists, columns=headers)
    return df
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    
    
    