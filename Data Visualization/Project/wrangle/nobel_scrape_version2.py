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

##############################################################################
## Uncomment to scrape all names/bios.
#
# scrape_birthdays_page(url, csv_name)
#
##############################################################################

nobel = pd.read_csv('../data/nobel_info.csv')
nobel = nobel.fillna("NA")

# Fix the entries where there was no reported city of death.
nobel.died_city[nobel.died_city.str.contains('span')] = "NA"

# Strip whitespace before comparing name to name_check.
nobel.name = nobel.name.str.strip()
nobel.name_check = nobel.name_check.str.strip()
# Also strip nobel field names


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
nobel['institution'], nobel['award_city'] = \
zip(*nobel['location_at_award'].apply(grab_inst_country_citystate))

# Fix records missing city info on nobelprize.org
nobel.query('location_at_award == "University of Delaware, USA"')
nobel.award_city[nobel.location_at_award == 'University of Delaware, USA'] = 'Newark, DE, USA'
nobel.award_city[nobel.award_city == 'Tunis'] = 'Tunis, Tunisia'

nobel.born_city[nobel.born_city == 'China'] = 'Changchung, China'
nobel.born_city[nobel.born_city == 'Trinidad'] = 'Chaguanas, Trinidad and Tobago'

# Locality changed due to new name or error in lookup.
nobel.born_city[nobel.born_city == 'Hofei, Anhwei, China'] = 'Hefei, Anhui, China'
nobel.born_city[nobel.born_city == 'Thorshavn, Faroe Islands (Denmark)'] = 'Torshavn, Faroe Islands'
nobel.born_city[nobel.born_city == 'Fleräng, Sweden'] = 'Flerängsvägen, Sweden'
nobel.born_city[nobel.born_city == "Taktser, People's Republic of China"] = 'Taktser, Qinghai, China'
nobel.born_city[nobel.born_city == "Nitzkydorf, Banat, Romania"] = 'Nitchidorf, Romania'
nobel.born_city[nobel.born_city == "Casteldàwson, Northern Ireland"] = 'Castledawson, Northern Ireland'
nobel.born_city[nobel.born_city == "Bad Salzbrunn, Germany"] = 'Szczawno-Zdrój, Poland'

# Fix some records that are missing info on the website.
nobel.query('location_at_award == "None"')
# Marie Curie was not affiliated with a university, but received the award 
# jointly with her husband who was affiliated with/at a uni in Paris, France.
nobel.award_city[(nobel.location_at_award == 'None') & (nobel.year_won == 1903)] = 'Paris, France'
nobel.location_at_award[(nobel.location_at_award == 'None') & (nobel.year_won == 1903)] = 'None, Paris, France'

# Working at UofM-AN form 1981 onward, awarded in 1999.
nobel.location_at_award[nobel.name == 'Martinus J.G. Veltman'] = 'University of Michigan-Ann Arbor, Ann Arbor, MI, USA'
nobel.award_city[nobel.name == 'Martinus J.G. Veltman'] = 'Ann Arbor, MI, USA'
nobel.institution[nobel.name == 'Martinus J.G. Veltman'] = 'University of Michigan-Ann Arbor'

# Worked at this corp when received. got $10,000 bonus.
nobel.location_at_award[nobel.name == 'Kary B. Mullis'] = 'Cetus Corporation, Emeryville, California'
nobel.award_city[nobel.name == 'Kary B. Mullis'] = 'Emeryville, California'
nobel.institution[nobel.name == 'Kary B. Mullis'] = 'Cetus Corporation'

# Retired at the time living in Chestefield. - NYTimes.com
nobel.location_at_award[nobel.name == 'William S. Knowles'] = 'None - retired, Chesterfield, MO, USA'
nobel.award_city[nobel.name == 'William S. Knowles'] = 'Chesterfield, MO, USA'
nobel.institution[nobel.name == 'William S. Knowles'] = 'None'

# Awarded jointly with colleague while at UofWA with colleague.
nobel.location_at_award[nobel.name == 'J. Robin Warren'] = 'University of Western Australia, Perth, Australia'
nobel.award_city[nobel.name == 'J. Robin Warren'] = 'Perth, Australia'
nobel.institution[nobel.name == 'J. Robin Warren'] = 'University of Western Australia'

# Living in Paris, France at the time of award
nobel.location_at_award[nobel.name == 'Ivan Alekseyevich Bunin'] = 'None, Paris, France'
nobel.award_city[nobel.name == 'Ivan Alekseyevich Bunin'] = 'Paris, France'
nobel.institution[nobel.name == 'Ivan Alekseyevich Bunin'] = 'None'

# Became a citizen of Spain in 1993, lived most of time there thereafter, awarded 2010
nobel.location_at_award[nobel.name == 'Mario Vargas Llosa'] = 'None, Madrid, Spain'
nobel.award_city[nobel.name == 'Mario Vargas Llosa'] = 'Madrid, Spain'
nobel.institution[nobel.name == 'Mario Vargas Llosa'] = 'None'

# Working at University of Salzburg 1969-1977, awarded 1974
nobel.location_at_award[nobel.name == 'Friedrich August von Hayek'] = 'University of Salzburg, Salzburg, Austria'
nobel.award_city[nobel.name == 'Friedrich August von Hayek'] = 'Salzburg, Austria'
nobel.institution[nobel.name == 'Friedrich August von Hayek'] = 'University of Salzburg'

# Spent his professional life working at Stockholm University
nobel.location_at_award[nobel.name == 'Gunnar Myrdal'] = 'Stockholm University, Stockholm, Sweden'
nobel.award_city[nobel.name == 'Gunnar Myrdal'] = 'Stockholm, Sweden'
nobel.institution[nobel.name == 'Gunnar Myrdal'] = 'Stockholm University'

# Le Duc Tho - located in North Vietnam. Fix error in lookup
nobel.award_city[nobel.award_city == 'Democratic Republic of Vietnam'] = 'North Vietnam'

##############################################################################
# 
# 
# nobel.to_csv('../data/nobel_info_updated.csv, index=FALSE')
##############################################################################






all_cities = set(nobel.born_city).union( set(nobel.award_city) )
# all_cities.remove('None')
all_cities = list(all_cities)
# Those without ',' are most likely just countries from peace/literature awards
just_countries = [x for x in all_cities if len(x.split(',')) <= 1]

##############################################################################
# coords = find_lon_lat_to_df(all_cities)

# Fix some records.
# coords.country[coords.location == "Nicosia, Cyprus"] = "Republic of Cyprus"
# coords.country_short_name[coords.location == "Nicosia, Cyprus"] = "CY"
# coords.country_short_name[coords.location == "Wailacama, East Timor"] = "TL"
# coords.country[coords.location == "Wailacama, East Timor"] = "Timor-Leste"

# City currently not grabbed. Empty.
#del coords['city_name']

# coords.to_csv('../data/nobel_coords.csv', index=False)
##############################################################################
coords = pd.read_csv('../data/nobel_coords.csv')


nobel_locations = pd.merge(nobel, coords, left_index=True, how='inner',
                        left_on=['born_city'], right_on=['location'])

nobel_locations = nobel_locations.reset_index(drop=True)      
                   
del nobel_locations['location'] # Delete location key

nobel_locations.rename(columns={'lon':'born_lon', 'lat':'born_lat',
                                'country':'born_country', 
                                'country_short_name': 'born_ctry_short_name'},
                                inplace=True)
                                
nobel_locations = pd.merge(nobel_locations, coords, left_index=True, how='inner',
                        left_on=['award_city'],
                        right_on=['location'])

del nobel_locations['location'] # Delete location key
nobel_locations = nobel_locations.reset_index(drop=True) 
nobel_locations.rename(columns={'lon':'award_lon', 'lat':'award_lat',
                                'country':'award_country', 
                                'country_short_name': 'award_ctry_short_name'},
                                inplace=True)
                                
# Strip whitespace from nobel field names                                
nobel_locations.nobel_field = nobel_locations.nobel_field.str.strip() 
nobel_locations = nobel_locations.reset_index(drop=True)    

nobel_locations.nobel_field[nobel_locations.nobel_field == \
 'The Nobel Prize in  Literature'] = 'The Nobel Prize in Literature'
nobel_locations['nobel_field_short'] = nobel_locations.nobel_field.map(map_field)
##############################################################################
# nobel_locations.to_csv('../data/nobel_locations.csv', index=False)
##############################################################################

nobel_locations = pd.read_csv('../data/nobel_locations.csv')

country_ISO = pd.read_csv('../data/wikipedia-iso-country-codes.csv')
country_ISO_2 = country_ISO[['Alpha-2 code', 'Numeric code']]

country_ISO_2.columns = ['ISO_alpha2', 'ISO_num']
country_ISO_2 = country_ISO_2[pd.notnull(country_ISO_2['ISO_alpha2'])]

nobel_locations = pd.merge(nobel_locations, country_ISO_2, left_index=True, 
                           how='inner',
                           left_on=['award_ctry_short_name'],
                           right_on=['ISO_alpha2'])
                           
nobel_locations = nobel_locations.reset_index(drop=True)

del nobel_locations['ISO_alpha2'] # Delete join key   

nobel_locations.rename(columns={'award_ctry_short_name':'award_ISO_alpha2', 
                                'ISO_num': 'award_ISO_num'}, inplace=True)
                        
##############################################################################
# nobel_locations.to_csv('../data/nobel_locations.csv', index=False)
##############################################################################
