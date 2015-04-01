# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:31:07 2015

@author: fch
"""
import requests
import json
import prettytable
import csv
import codecs
import requests
import pandas as pd
import sys  


from bs4 import BeautifulSoup
from wrangle import *
from latlon import *

reload(sys)
sys.setdefaultencoding("utf-8")

url = 'http://www.nobelprize.org/nobel_prizes/lists/universities.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, from_encoding=r.encoding)
acquired_html = soup.find_all(name="div", attrs={"class": "by_year"})

nobel_acquired = find_country_acq(acquired_html)
###############################################################################
#acq_lat_lon = create_lat_lon(nobel_acquired, country_type='acquired', 
#                             country_col='current_country_name_acquired',
#                             city_col='city', state_col='state')
###############################################################################
nobel_acquired2 = pd.merge(nobel_acquired, acq_lat_lon)



url2 = 'http://www.nobelprize.org/nobel_prizes/lists/age.html'
r2 = requests.get(url2)
soup2 = BeautifulSoup(r2.text)
age_html = soup2.find_all(name="div", attrs={"class": "large-12 columns"})

nobel_ages = find_age(age_html)


url3 = 'http://www.nobelprize.org/nobel_prizes/lists/countries.html'
r3 = requests.get(url3)
soup3 = BeautifulSoup(r3.text)
birth_html = soup3.find_all(name="div", attrs={"class": "by_year"})

nobel_birth = find_country_birth(birth_html)
##############################################################################
#birth_lat_lon = create_lat_lon(nobel_birth, country_type='birth', 
#                               country_col='birth_country_current_name')
##############################################################################
nobel_birth2 = pd.merge(nobel_birth, birth_lat_lon)
del nobel_birth2['city']
del nobel_birth2['state']

sorted1 = nobel_birth2.sort(columns=['name', 'year']).reset_index(drop=True)
sorted2 = nobel_ages.sort(columns=['name', 'age']).reset_index(drop=True)
merged = pd.merge(sorted1, sorted2, left_index=True, right_index=True, how='outer', on='name')
# merged[merged.name=="Marie Curie"]
all_acquired = pd.merge(nobel_acquired2, merged, left_index=True, 
                        how='inner', on=['name', 'year', 'field'])
                        
##############################################################################                        
#all_acquired.to_csv('data/all_acquired.csv', encoding='utf-8')

nobel_peace = merged[merged['field'] == 'Peace']
#nobel_peace.to_csv('data/nobel_peace.csv', encoding='utf-8')
##############################################################################













#headers = country_acquired.pop(0)
#df = pd.DataFrame(country_acquired, columns=headers)
#df.head()


#countries = list(set(df.birth_country_new_name))

# url2 = lookup_lat_lon(country=countries[38], key=google_api_key)
# r2 = requests.get(url2)
# country_json = r2.json()

# Get the lat/lon from the Google API!
#lat_lon_birth_countries = get_long_lat(countries, birth_countries=True)

#headers = lat_lon_birth_countries.pop(0)
#birth_countries_df = pd.DataFrame(lat_lon_birth_countries, columns=headers)
#birth_countries_df.head()