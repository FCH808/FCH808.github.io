
# coding: utf-8

# In[2]:

import requests
import json
import prettytable
import csv
import codecs

from bs4 import BeautifulSoup
# In[ ]:




# In[3]:





# In[4]:

url = 'http://www.nobelprize.org/nobel_prizes/lists/universities.html'
r = requests.get(url)
soup = BeautifulSoup(r.text)
place_acquired = soup.find_all(name="div", attrs={"class": "by_year"})


# In[516]:




# In[7]:

def grab_field_and_number(string):
    '''
    >>>grab_field_and_number("The Nobel Prize in Physics 2000")
    ('2000', 'Physics')
    
    >>>grab_field_and_number("The Prize in Economic Sciences 2010")
    ('2010', 'Economic Sciences')
    
    >>>grab_field_and_number("The Nobel Prize in Physiology or Medicine 2000")
    ('2000', 'Physiology or Medicine')
    
    >>>grab_field_and_number("The Nobel in Peace Prize 2010")
    ('2010', 'Peace')
    '''
    
    if "Economic" in string:
        temp_string = string.split()
        year = temp_string.pop()
        field = temp_string[-2] + " " + temp_string[-1]
    elif "Physiology or Medicine" in string:
        temp_string = string.split()
        year = temp_string.pop()
        field = temp_string[-3] + " " + temp_string[-2] + " " + temp_string[-1]
    elif "Peace" in string:
        temp_string = string.split()
        year = temp_string.pop()
        field = temp_string[-2]
    else:
        temp_string = string.split()
        year = temp_string.pop()
        field = temp_string[-1]
    return year, field



# In[8]:

grab_field_and_number("The Nobel in Peace Prize 2010")


# In[9]:

#grab_field_and_number("The Nobel Prize in Physics 2000")


# In[10]:

#grab_field_and_number("The Prize in Economic Sciences 2010")


# In[11]:

#grab_field_and_number("The Nobel Prize in Physiology or Medicine 2000")


# In[12]:

def grab_inst_country_citystate(string):
    '''
    >>>grab_inst_citystate_country("Edinburgh University, Edinburgh, United Kingdom")
    ('Edinburgh University', ' United Kingdom', ' Edinburgh', '', '')
    
    >>>grab_inst_country_citystate("Fred Hutchinson Cancer Research Center, Seattle, WA, USA")
    ('Fred Hutchinson Cancer Research Center', ' USA', ' WA', ' Seattle', '')
    
    >>>grab_inst_country_citystate("Columbia University Division, Cardio-Pulmonary Laboratory, Bellevue Hospital, New York, NY, USA")
    ('Columbia University Division',
 ' USA',
 ' NY',
 ' New York',
 ' Cardio-Pulmonary Laboratory,  Bellevue Hospital')
    '''
    pieces = string.split(",")
    institution = pieces[0]
    country = pieces[-1]
    city_state = pieces[1:-1]
    city, state, extra_loc = grab_city_state(city_state)
    return institution, country, city, state, extra_loc


# In[13]:

#grab_inst_citystate_country("Edinburgh University, Edinburgh, United Kingdom")


# In[14]:

#grab_inst_country_citystate("Fred Hutchinson Cancer Research Center, Seattle, WA, USA")


# In[15]:

#grab_inst_country_citystate("Columbia University Division, Cardio-Pulmonary Laboratory, Bellevue Hospital, New York, NY, USA")


# In[16]:

def grab_city_state(a_list):
    '''
    >>>grab_city_state(["Cardio-Pulmonary Laboratory", "Bellevue Hospital", "New York", "NY"])
    ('NY', 'New York', 'Cardio-Pulmonary Laboratory, Bellevue Hospital')
    
    >>>grab_city_state(["Bellevue Hospital", "New York", "NY"])
    ('NY', 'New York', 'Bellevue Hospital')
    
    >>>grab_city_state(['New York', 'NY'])
    grab_city_state(['New York', 'NY'])
    
    >>>grab_city_state(['New York'])
    ('New York', '', '')    
    '''
    city = a_list.pop()
    state = ""    
    other = ""
    if len(a_list) >= 1:
        state = a_list.pop()
        other = ", ".join(a_list)
    return city, state, other


# In[17]:

#grab_city_state(["Cardio-Pulmonary Laboratory", "Bellevue Hospital", "New York", "NY"])


# In[18]:

#grab_city_state(["Bellevue Hospital", "New York", "NY"])


# In[19]:

#grab_city_state(['New York', 'NY'])


# In[20]:

#grab_city_state(['New York'])


# In[ ]:




# In[223]:

def separate_old_country_names(country):
    old = ""
    new = ""
    if " (now " in country:
        old_and_new = country.split(' (now ')
        old = old_and_new[0]
        new = old_and_new[1][:-1]
    else:
        old = country
        new = country
    return old, new
            


# In[274]:

def find_country_acq(bs4_html):
    all_names = [["name", "institution",
                  "old_country_name_acquired","current_country_name_acquired",
                  "city","state", "extra_loc_info","year","field"]]
    place_acq = ""
    for i in bs4_html:
        #pprint.pprint(i) 
        #print "*"*80
        #print i
        if i.find_all('h3'):
            #print "i.TEXT: ", i.text
            place_acq = i.h3.text
        if i.find_all('a'):
            #print ""
            #print "i.a.TEXT: ", i.a.text
            #print "i.h6.TEXT: ", i.h6.text
            #print "PLACE_ACQ: ", place_acq
            #print "field_year: ", field_year
            field_year = i.a.text
            name = i.h6.text
            year, field = grab_field_and_number(field_year)
            institution, country, city, state, extra_loc = grab_inst_country_citystate(place_acq)
            
            old_country_name, new_country_name = separate_old_country_names(country)
            
            all_names.append([name.encode('utf-8'), 
                              institution.encode('utf-8'),
                              old_country_name.encode('utf-8'),
                              new_country_name.encode('utf-8'),
                              city.encode('utf-8'),
                              state.encode('utf-8'),
                              extra_loc('utf-8'),
                              year.encode('utf-8'),
                              field.encode('utf-8')])
            
            #print ""
            #print "*"*80
    return all_names


# In[275]:

len(find_country_acq(place_acquired))


# In[276]:




# In[23]:

url = 'http://www.nobelprize.org/nobel_prizes/lists/countries.html'
r = requests.get(url)
soup = BeautifulSoup(r.text)
birth_html = soup.find_all(name="div", attrs={"class": "by_year"})


# In[23]:




# In[283]:

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
            
            all_names.append([name.encode('utf-8'), 
                              old_country_name.encode('utf-8'),
                              new_country_name.encode('utf-8'),
                              year.encode('utf-8'),
                              field.encode('utf-8')])
            
    return all_names


# In[229]:

len(find_country_birth(birth_html))


# In[25]:




# In[25]:




# In[26]:

url = 'http://www.nobelprize.org/nobel_prizes/lists/age.html'
r = requests.get(url)
soup = BeautifulSoup(r.text)
age_html = soup.find_all(name="div", attrs={"class": "large-12 columns"})


# In[85]:

def find_age(bs4_html):
    all_names = [["name", "age"]]
    place_acq = ""
    for i in age_html[6].find_all(['h3', 'h6']):
        
        if "Age" in i.string:
            age = i.string.split()[-1]
        if "Age" not in i.string:
            name = i.string
            all_names.append([name.encode('utf-8'), age.encode('utf-8')])
    return all_names


# In[86]:

len(find_age(age_html))


# In[88]:

nobel_ages = find_age(age_html)


# In[89]:

with open('nobel_ages.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(nobel_ages)


# In[226]:

country_acquired = find_country_acq(place_acquired)


# In[111]:

#country_acquired


# In[118]:




# In[119]:


#country_birth


# In[314]:

import pandas as pd

country_birth = find_country_birth(birth_html)
headers = country_birth.pop(0)
df = pd.DataFrame(country_birth, columns=headers)
df.head()


# In[236]:

countries = list(set(df.birth_country_new_name))


# In[238]:

#google_api_key = "AIzaSyDAJxRxTE-ZC5M7qGN5Bg_FXwgc5e_TqdU"


# In[239]:

def lookup_lat_lon(city="", state="", country="", key=""):
    return "https://maps.googleapis.com/maps/api/geocode/json?"+"address="+country+"&key="+key


# In[288]:

lookup_lat_lon(country=countries[38], key=google_api_key)


# In[289]:

url2 = lookup_lat_lon(country=countries[38], key=google_api_key)


# In[290]:

r2 = requests.get(url2)


# In[291]:

country_json = r2.json()


# In[292]:

birth_lat = country_json['results'][0]['geometry']['location']['lat']
birth_lon = country_json['results'][0]['geometry']['location']['lng']
birth_country_long_name = country_json['results'][0]['address_components'][0]['long_name']
birth_country_short_name = country_json['results'][0]['address_components'][0]['short_name']


# In[296]:

print birth_lat
print birth_lon
#birth_country_long_name


# In[295]:

#country_json


# In[315]:

def get_long_lat(country_list, birth_countries=True):
    
    output = [['birth_lat', 
               'birth_lon', 
               'birth_country_current_name',
               'birth_country_short_name']]
    if birth_countries == False:
        output = [['acquired_lat', 
                   'acquired_lon', 
                   'current_country_name_acquired',
                   'acquired_country_short_name']]
    # https://console.developers.google.com
    # https://developers.google.com/maps/documentation/geocoding/?csw=1
    google_api_key = "AIzaSyDAJxRxTE-ZC5M7qGN5Bg_FXwgc5e_TqdU"
    
    for each_country in country_list:
        url = lookup_lat_lon(country=each_country, key=google_api_key)
        r = requests.get(url)
        country_json = r.json()
        lat = country_json['results'][0]['geometry']['location']['lat']
        lon = country_json['results'][0]['geometry']['location']['lng']
        #country_long_name = country_json['results'][0]['address_components'][0]['long_name']
        country_long_name = each_country
        country_short_name = country_json['results'][0]['address_components'][0]['short_name']
        
        output.append([lat,
                       lon,
                       country_long_name,
                       country_short_name])
    return output


# In[307]:

# Get the lat/lon from the Google API!
lat_lon_birth_countries = get_long_lat(countries, birth_countries=True)


# In[308]:

headers = lat_lon_birth_countries.pop(0)
birth_countries_df = pd.DataFrame(lat_lon_birth_countries, columns=headers)


# In[313]:

birth_countries_df.head()


# In[397]:

df = pd.merge(df, birth_countries_df)
df.tail()


# In[398]:

# df.to_csv('data/temp.csv')


# In[319]:

headers = nobel_ages.pop(0)
nobel_ages_df = pd.DataFrame(nobel_ages, columns=headers)


# In[384]:

#pd.merge(df, nobel_ages_df).tail(20)


# Since 4 people won Nobel Prizes twice (!) at different ages, these dataframes can't just be merged on the 'name' column. Instead, we can sort/reorder each dataframe by the names and year/age, resetting the index to get them aligned.
# 
# Now, we can merge(or join()) them in pandas on the indices of each dataframe. Now, we can see Marie Curie was age 36 when recieving the nobel when recieving the Nobel Prize in 1903 in Physics, then 44 in 1911 when recieving the Nobel Prize in Chemistry.

# In[399]:

sorted1 = df.sort(columns=['name', 'year']).reset_index(drop=True)
sorted2 = nobel_ages_df.sort(columns=['name', 'age']).reset_index(drop=True)
merged = pd.merge(sorted1, sorted2, left_index=True, right_index=True,
                  how='outer', on='name')
merged[merged.name == "Marie Curie"]


# In[401]:

merged.to_csv('data/temp.csv', encoding='utf-8')


# In[402]:

merged.head()


# In[403]:




# In[404]:




# In[405]:




# In[ ]:




# In[ ]:



