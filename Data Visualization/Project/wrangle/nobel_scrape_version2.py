# -*- coding: utf-8 -*-
"""
Created on Fri Apr 03 16:30:05 2015

@author: fch
"""

import pandas as pd
import sys
from wrangle import scrape_birthdays_page, get_current_loc
from wrangle import grab_inst_country_citystate
from latlon import *

reload(sys)
sys.setdefaultencoding("utf-8")

url = "http://www.nobelprize.org/nobel_prizes/lists/birthdays.html?day=0&month=0&year=&photo=1#birthday_result"
csv_name = "../data/nobel_info.csv"

scrape_birthdays_page(url, csv_name)


nobel = pd.read_csv('../data/nobel_info.csv')
nobel = nobel.fillna("NA")

# Fix the entries where there was no reported city of death.
nobel.died_city[nobel.died_city.str.contains('span')] = "NA"

# Strip whitespace before comparing name to name_check.
nobel.name = nobel.name.str.strip()
nobel.name_check = nobel.name_check.str.strip()

# All names match the name_check from each bio page.
nobel[nobel['name'] != nobel['name_check']][['name', 'name_check']]

# Drop the name_check once confirmed.
del nobel['name_check']

# Strip the leading ', ' in city names.
nobel.born_city = nobel.born_city.str.strip(', ')
nobel.died_city = nobel.died_city.str.strip(', ')

nobel.born_city = nobel.born_city.apply(get_current_loc)
nobel.died_city = nobel.died_city.apply(get_current_loc)

# Create two columns with the output from function that splits institution
# string into institution and the institution city location.
nobel['institution'], nobel['inst_city'] = \
zip(*nobel['affiliation'].apply(grab_inst_country_citystate))

# Fix records missing city info on nobelprize.org
nobel.query('inst_city == "USA"')
nobel.inst_city[nobel.inst_city == 'USA'] = 'Newark, DE, USA'
nobel.inst_city[nobel.inst_city == 'Tunis'] = 'Tunis, Tunisia'

nobel.born_city[nobel.born_city == 'China'] = 'Changchung, China'
nobel.born_city[nobel.born_city == 'Trinidad'] = 'Chaguanas, Trinidad and Tobago'

# Locality changed due to error in lookup.
nobel.born_city[nobel.born_city == 'Hofei, Anhwei, China'] = 'Hefei, Anhui, China'
nobel.born_city[nobel.born_city == 'Thorshavn, Faroe Islands (Denmark)'] = 'Torshavn, Faroe Islands'
nobel.born_city[nobel.born_city == 'Fleräng, Sweden'] = 'Flerängsvägen, Sweden'
nobel.born_city[nobel['born_city'] == "Taktser, People's Republic of China"] = 'Taktser, Qinghai, China'


all_cities = set(nobel.born_city).union( set(nobel.inst_city) )
all_cities.remove('None')
all_cities = list(all_cities)
# No more single words in the list of all born and institution cities
sum(len(x.split(',')) <= 1 for x in all_cities)

all_acquired = pd.merge(nobel, df, left_index=True, how='inner',
                        left_on=['born_city'], right_on=['location'])

all_acquired.rename(columns={'lon':'born_lon', 'lat':'born_lat'}, inplace=True)

all_acquired = pd.merge(all_acquired, df, left_index=True, how='inner',
                        left_on=['inst_city'], right_on=['location'])
                        
all_acquired.rename(columns={'lon':'inst_lon', 'lat':'inst_lat'}, inplace=True)