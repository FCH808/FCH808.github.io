# -*- coding: utf-8 -*-
"""
Spyder Editor


"""
import pandas as pd
from latlon import *
import re
from bs4 import BeautifulSoup
import csv
import sys
import requests

def scrape_birthdays_page(url=None, csv_name=None):
    """ Scrape info from nobelprize.org birthdays page
    
    Scrapes info from the birthdays page at:
        http://www.nobelprize.org/nobel_prizes/lists/birthdays.html?day=0&month=0&year=&photo=1#birthday_result
    
    Also scrapes each bio_page of each winner for more info.
    
    Writes to csv: thumbnail pic URL,
            bio url link,
            name
            Year Prize Won
            Nobel Prize field
            Year Born
            Year Died
            Name again (sync check)
            Born City
            Died City (if applicable)
            Affiliation at time of award
            
    Args:
        url: HTML url to nobelprize.org birthdays page 
        csv_out_name: String with name of csv file name to write to
    Returns:
        Write csv file to name specified in csv_out_name
    
    """
    
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text, from_encoding=r.encoding)

    each_entry_divs = soup.find_all("div", attrs={"class":"row", "style": "margin-bottom: 15px;"})
    
    each_entry_divs.pop(0)
    
    f = csv.writer(open(csv_name, "wb"))
    f.writerow(["name", "bio_thumbnail", "bio_link", "year_won",
                "nobel_field", "year_born", "year_died", "name_check",
                "born_city", "died_city", "location_at_award"])
    
    for person in each_entry_divs:
        
        bio_thumbnail = person.find("img")['src']
    
        bio_link = person.find(class_='text_link')['href']
        
        nobel_info = person.find_all(class_="medium-10 columns birthdays-result-main")[0].text.split('\n')

        year_won = nobel_info[0].split(",")[0]
        nobel_field = nobel_info[0].split(",")[1]
        # Get rid of extra spaces between some words.
        ## TODO; uncomment later to redo all scrapes.
        nobel_field = " ".join([x.strip() for x in nobel_field.split()])
        name = nobel_info[1]
        year_born = nobel_info[2].split(":")[1]

        
        try:
            year_died = nobel_info[3].split(":")[1]
        except IndexError as e:
            year_died = ""           
        
        
        bio_link_full = "http://www.nobelprize.org/" + bio_link
        name_check, born_city, died_city, affiliation = scrape_bio_page(bio_link_full)
        

        f.writerow([name, bio_thumbnail, bio_link, year_won, 
                    nobel_field, year_born, year_died, name_check,
                    born_city, died_city, affiliation])


def scrape_bio_page(url=None):
    '''Scrape Novel prize winner bio page for info.
    
    Scrapes info from nobelprize.org bio-pages.
    Info includes: name,
                   born_location,
                   died_location,
                   affiliation at time of award/ country of residence
                   
    
    Args:
        url: Nobelprize.org Bio page to scrape.
    Returns:
        Four string (may be empty if not present): name, born_location, 
                                                   died_location, institution
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, from_encoding=r.encoding)    
    
    name = soup.find_all(attrs={'itemprop': 'Name'})[0].text
    # Find the birthdate node, get its parent, then get the last string in the 
    # contents which has the city.
    born_city = soup.find_all(attrs={'itemprop': 'birthDate'})[0].parent.contents[-1]
    try:    
        death_city = soup.find_all(attrs={'itemprop': 'deathDate'})[0].parent.contents[-1]
    except IndexError as e:
        death_city = ""

    affiliation = "None"

    
    try:
        # Peace/Literature Prizes generally have residences at time of award
        # but no institution.
        residence = soup.find_all('strong', text='Residence at the time of the award:')[0].parent.contents[-1]
        affiliation = "None, " + residence
    except IndexError as e:    
        pass
    
    try:
        # Overwrite None or Country of Residence with city affiliation if avail.
        affiliation = soup.find_all(attrs={'itemprop': 'affiliation'})[0].contents[-1]
    except IndexError as e:
        pass

        
    return name, born_city, death_city, affiliation


    
#def find_country_birth(bs4_html):
#    all_names = [["name","birth_country_old_name",
#                  "birth_country_current_name",
#                  "year","field"]]
#    place_acq = ""
#    for i in bs4_html:
#        # Only place acquired entries have an 'h3' sub-class
#        if i.find_all('h3'):
#            place_acq = i.h3.text
#        # Only field_year/name entries have an 'h6' sub-class.
#        if i.find_all('h6'):
#            field_year = i.a.text
#            name = i.h6.text
#            year, field = grab_field_and_number(field_year)
#            old_country_name, new_country_name = separate_old_country_names(place_acq)
#            
#            all_names.append([name.encode('utf-8').strip(), 
#                              old_country_name.encode('utf-8').strip(),
#                              new_country_name.encode('utf-8').strip(),
#                              year.encode('utf-8').strip(),
#                              field.encode('utf-8').strip()])
#            
#    return df_from_lists(all_names, header_included=True)

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
    
    >>> grab_city_state(["Cardio-Pulmonary Laboratory", "Bellevue Hospital", "New York", "NY"], 'USA')
    ('New York', 'NY', 'Cardio-Pulmonary Laboratory, Bellevue Hospital')
    
    >>> grab_city_state(["Bellevue Hospital", "New York", "NY"], 'USA')
    ('New York', 'NY', 'Bellevue Hospital')
    
    >>> grab_city_state(['New York', 'NY'], 'USA')
    ('New York', 'NY', '')
    
    >>> grab_city_state(['New York'], 'USA')
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

    return city.strip(), state.strip(), other.strip()

def grab_inst_country_citystate(location):
    '''
    
    >>> grab_inst_country_citystate("Edinburgh University, Edinburgh, United Kingdom")
    ('Edinburgh University', 'Edinburgh, United Kingdom')
    
    >>> grab_inst_country_citystate("Fred Hutchinson Cancer Research Center, Seattle, WA, USA")
    ('Fred Hutchinson Cancer Research Center', 'Seattle, WA, USA')
    
    >>> grab_inst_country_citystate("Columbia University Division, Cardio-Pulmonary Laboratory, Bellevue Hospital, New York, NY, USA")
    ('Bellevue Hospital', 'New York, NY, USA')
    
    >>> grab_inst_country_citystate('Strasbourg University, Strasbourg, Alsace (then Germany, now France)')
    ('Strasbourg University', 'Strasbourg, France')


    '''
    # Handle corner case.
    location = location.replace('then Germany, ', '')
    # Handle record with missing data.
    if location == 'Howard Hughes Medical Institute, , ':
        print location
        location = 'Howard Hughes Medical Institute, Chevy Chase, MD, USA'  
    # Many locations end with HHMI, while still having other locations.
    if location[-33:] == ', Howard Hughes Medical Institute':
        location = location[0:-33]
    
    pieces = location.split(",")    
    pieces = [each.strip() for each in pieces]
    # Many strings have two associated universities 
    
    # Some strings have 2 locations in them. Handle these differently.
    # Using only the second location.
    if len(pieces) >= 6:
        # If USA is present, there may will be a state.
        if "USA" == pieces[-1]:
            institution = pieces[-4]
            city = pieces[-3]
            state = pieces[-2]
            country = pieces[-1]
            extra_loc = ""
        else:
            institution = pieces[-3]
            city = pieces[-2]
            state = ""
            country = pieces[-1]
            extra_loc = ""
    else:
        # Otherwise, process differently
        institution = pieces[0]
        country = pieces[-1]
        city_state = pieces[1:-1]
        city, state, extra_loc = grab_city_state(city_state, country)
    

            
    # Fix problem records for Google map api lookup.
    if country == "USSR":
        country = "Russia"
    if country == "Czechoslovakia":
        country = "Czech Republic"
        
    # Don't use any 'extra location' info for now. 
        
    # institution = ', '.join(filter(None, [institution, extra_loc]))
    location = ', '.join(filter(None, [city, state, country]))
    location = get_current_loc(location)
    return institution, location
    
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
 

def get_current_loc(location_string):
    '''Returns string of updated location.
    
    Pulls out the updated location (now newLocation) from the location
        to pass to Google Maps api for lon/lat coordinates.
        
    Args:
        location_string: String with location, with possible current updates.
    Returns:
        string of the updated location only.
    
    '''
    
    location = []    
    if '(now ' in location_string:
        temp = location_string.split(',')
        location = []
        for word in temp:
            if "(now " in word:
                word = word.split('(now ')[1].strip(')')
            location.append(word)
    else:
        # If (now not present, just return the original string)
        return location_string    
    return ", ".join(word for word in location)
   
def map_field(x):
    if x == 'The Nobel Prize in Literature':
        return "literature"
    elif x == 'The Nobel Prize in Chemistry':
        return "chemistry"
    elif x == 'The Nobel Prize in Physics':
        return "physics"
    elif x == 'The Nobel Prize in Physiology or Medicine':
        return "physiology"
    elif x == 'The Sveriges Riksbank Prize in Economic Sciences in Memory of Alfred Nobel':
        return "economics"
    elif x == 'The Nobel Peace Prize':
        return "peace"


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
    
    
    
    