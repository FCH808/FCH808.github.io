# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 13:46:12 2014

@author: fch
"""

import pandas as pd
import pandasql
import csv

filename="..\\data\\turnstile_data_master_with_weather.csv"


## Question 2.1
def num_rainy_days(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - a count of the number of days in the dataframe where
    the rain column is equal to 1 (i.e., the number of days it
    rained).  The dataframe will be titled 'weather_data'. You'll
    need to provide the SQL query.  You might find SQL's count function
    useful for this exercise.  You can read more about it here:
    
    https://dev.mysql.com/doc/refman/5.1/en/counting-rows.html
    
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be equal to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    '''
    weather_data = pd.read_csv(filename)
    weather_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)

## Correct Grader Solution:    
#    q = """
#    SELECT count(*)
#    FROM weather_data
#    WHERE cast(rain as integer) = 1
#    """    
## 

    
## Correct grader solution only works on the very small 30x70 dataframe with unique dates. 
## Below query works on full turnstile dataset provided to us.    
    
    q = """
    SELECT COUNT(DISTINCT DATEn) as 'count(*)'
    FROM weather_data 
    WHERE cast(rain as integer) = 1
    """
    
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q, locals())
    return rainy_days

#print num_rainy_days(filename)

## Question 2.2
def max_temp_aggregate_by_fog(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return two columns and
    two rows - whether it was foggy or not (0 or 1) and the max
    maxtempi for that fog value (i.e., the maximum max temperature
    for both foggy and non-foggy days).  The dataframe will be 
    titled 'weather_data'. You'll need to provide the SQL query.
    
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be useful to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    '''
    weather_data = pd.read_csv(filename)
    weather_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)    
    
    q = """
    SELECT fog, max(cast (maxtempi as integer)) as MaxTemp 
    FROM weather_data 
    GROUP BY fog;
    """
    
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q, locals())
    return rainy_days

# print max_temp_aggregate_by_fog(filename)

def avg_min_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - the average meantempi on days that are a Saturday
    or Sunday (i.e., the the average mean temperature on weekends).
    The dataframe will be titled 'weather_data' and the you can access
    the date in the dataframe via the 'date' column.
    
    You'll need to provide  the SQL query.
    
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be equal to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    
    Also, you can convert dates t\
    the week via the 'strftime' keyword in SQL.
    For example, cast (strftime('%w', date) as integer) will return 0 if the date
    is a Sunday or 6 if the date is a Saturday.
    '''
    weather_data = pd.read_csv(filename)
    weather_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)

## Correct Grader Solution:
#    q = """
#    SELECT AVG(cast (meantempi as integer))
#    FROM weather_data 
#    WHERE cast (strftime('%w', date) as integer) in (0, 6)
##  

    q = """
    SELECT AVG(cast (meantempi as integer))
    FROM weather_data 
    WHERE cast (strftime('%w', DATEn) as integer) in (0, 6)
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q, locals())
    return mean_temp_weekends

#print avg_min_temperature(filename)


def avg_min_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data. More specifically you want to find the average
    minimum temperature on rainy days where the minimum temperature
    is greater than 55 degrees.
    
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be equal to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    '''
    weather_data = pd.read_csv(filename)
    weather_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)

    q = """
    SELECT AVG(cast (mintempi as integer)) 
    FROM weather_data 
    WHERE mintempi > 55 
    AND rain = 1
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q, locals())
    return mean_temp_weekends

#print avg_min_temperature(filename)

def split_seq(seq, size):
    """ Split up seq in pieces of size """
    return [seq[i:i+size] for i in range(0, len(seq), size)]

filename=["turnstile_110528.txt"]

def fix_turnstile_data(filenames):
    '''
    Filenames is a list of MTA Subway turnstile text files. A link to an example
    MTA Subway turnstile text file can be seen at the URL below:
    http://web.mta.info/developers/data/nyct/turnstile/turnstile_110507.txt
    
    As you can see, there are numerous data points included in each row of the
    a MTA Subway turnstile text file. 

    You want to write a function that will update each row in the text
    file so there is only one entry per row. A few examples below:
    A002,R051,02-00-00,05-28-11,00:00:00,REGULAR,003178521,001100739
    A002,R051,02-00-00,05-28-11,04:00:00,REGULAR,003178541,001100746
    A002,R051,02-00-00,05-28-11,08:00:00,REGULAR,003178559,001100775
    
    Write the updates to a different text file in the format of "updated_" + filename.
    For example:
        1) if you read in a text file called "turnstile_110521.txt"
        2) you should write the updated data to "updated_turnstile_110521.txt"

    The order of the fields should be preserved. 
    
    You can see a sample of the turnstile text file that's passed into this function
    and the the corresponding updated file in the links below:
    
    Sample input file:
    https://www.dropbox.com/s/mpin5zv4hgrx244/turnstile_110528.txt
    Sample updated file:
    https://www.dropbox.com/s/074xbgio4c39b7h/solution_turnstile_110528.txt
    '''
    for one_file in filenames:

        with open(one_file, "r") as read_data:
              # Get rid of extra blank line.
              # Open outfile with mode 'wb' instead of 'w'.
              # The csv.writer writes \r\n into the file directly.
              # If you don't open the file in binary mode,
              #  it will write \r\r\n because on Windows text mode will translate each \n into \r\n.
            with open("updated_{}".format(one_file), "wb") as write_data:
                reader = csv.reader(read_data)
                writer = csv.writer(write_data)
                for line in reader:
                    header = line[:3]
                    clean_line = [s.strip() for s in line]
                    rest = [clean_line[i:i+5] for i in range(3, len(clean_line), 5)]

                    for each_one in rest:
                        writer.writerow(header + each_one)
            write_data.close()
        read_data.close()

#fix_turnstile_data(filename)

filenames = ["updated_turnstile_110528.txt", "updated_turnstile_110528.txt"]
output_file = "output.txt"

def create_master_turnstile_file(filenames, output_file):
    '''
    Write a function that takes the files in the list filenames, which all have the 
    columns 'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn', and consolidates
    them into one file located at output file.  There should be ONE row with the column
    headers, located at the top of the file.
    
    For example, if file_1 has:
    'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn'
    line 1 ...
    line 2 ...
    
    and another file, file_2 has:
    'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn'
    line 3 ...
    line 4 ...
    line 5 ...
    
    We need to combine file_1 and file_2 into a master_file like below:
     'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn'
    line 1 ...
    line 2 ...
    line 3 ...
    line 4 ...
    line 5 ...
    '''
    with open(output_file, 'w') as master_file:
       master_file.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
       for filename in filenames:
                with open(filename, 'r') as f:
                    ## discard header
                    f.readline()
                    content = f.read()
                    master_file.write(content)
                    f.close()
       master_file.close()
                    
# create_master_turnstile_file(filenames, output_file)

filename = filename="output.txt"

def filter_by_regular(filename):
    '''
    This function should read the csv file located at filename into a pandas dataframe,
    and filter the dataframe to only rows where the 'DESCn' column has the value 'REGULAR'.
    
    For eample, if the pandas dataframe is as follows:
    ,C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    1,A002,R051,02-00-00,05-01-11,04:00:00,DOOR,3144335,1088159
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    3,A002,R051,02-00-00,05-01-11,12:00:00,DOOR,3144424,1088231
    
    The dataframe will look like below after filtering to only rows where DESCn column
    has the value 'REGULAR':
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    '''
    
    turnstile_data = pd.read_csv(filename)
    #for DESCn, row in turnstile_data.iterrows():
    #    if row['DESCn'] == 'REGULAR'
    turnstile_data = turnstile_data[turnstile_data.DESCn == 'REGULAR']        
    
    
    return turnstile_data
    
#print filter_by_regular(filename)

#filename = filename="output.txt"
#df = pd.read_csv(filename)
#df = df[(df['SCP'] == '02-00-00') & (df['C/A']=='A002') & (df['UNIT']=='R051')]

def get_hourly_entries(df):
    '''
    The data in the MTA Subway Turnstile data reports on the cumulative
    number of entries and exits per row.  Assume that you have a dataframe
    called df that contains only the rows for a particular turnstile machine
    (i.e., unique SCP, C/A, and UNIT).  This function should change
    these cumulative entry numbers to a count of entries since the last reading
    (i.e., entries since the last row in the dataframe).
    
    More specifically, you want to do two things:
       1) Create a new column called ENTRIESn_hourly
       2) Assign to the column the difference between ENTRIESn of the current row 
          and the previous row. If there is any NaN, fill/replace it with 1.
    
    You may find the pandas functions shift() and fillna() to be helpful in this exercise.
    
    Examples of what your dataframe should look like at the end of this exercise:
    
           C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly
    0     A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                1
    1     A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23
    2     A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18
    3     A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71
    4     A002  R051  02-00-00  05-01-11  16:00:00  REGULAR   3144594   1088275              170
    5     A002  R051  02-00-00  05-01-11  20:00:00  REGULAR   3144808   1088317              214
    6     A002  R051  02-00-00  05-02-11  00:00:00  REGULAR   3144895   1088328               87
    7     A002  R051  02-00-00  05-02-11  04:00:00  REGULAR   3144905   1088331               10
    8     A002  R051  02-00-00  05-02-11  08:00:00  REGULAR   3144941   1088420               36
    9     A002  R051  02-00-00  05-02-11  12:00:00  REGULAR   3145094   1088753              153
    10    A002  R051  02-00-00  05-02-11  16:00:00  REGULAR   3145337   1088823              243
    ...
    ...

    '''
    # print df
    df['temp'] = df.ENTRIESn.shift(1)
    # df['ENTRIESn_hourly'] = 0
    #
    df['ENTRIESn_hourly'] = (df['ENTRIESn'] - df['temp'])
    # df = df.drop('ENTRIESn',1)
    del df['temp']
    df['ENTRIESn_hourly'].fillna(1, inplace=True)
    return df

#df = get_hourly_entries(df)
#print df.head()
## Question 2.9

def get_hourly_exits(df):
    '''
    The data in the MTA Subway Turnstile data reports on the cumulative
    number of entries and exits per row.  Assume that you have a dataframe
    called df that contains only the rows for a particular turnstile machine
    (i.e., unique SCP, C/A, and UNIT).  This function should change
    these cumulative exit numbers to a count of exits since the last reading
    (i.e., exits since the last row in the dataframe).
    
    More specifically, you want to do two things:
       1) Create a new column called EXITSn_hourly
       2) Assign to the column the difference between EXITSn of the current row 
          and the previous row. If there is any NaN, fill/replace it with 0.
    
    You may find the pandas functions shift() and fillna() to be helpful in this exercise.
    
    Example dataframe below:

          Unnamed: 0   C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly  EXITSn_hourly
    0              0  A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                0              0
    1              1  A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23              8
    2              2  A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18             18
    3              3  A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71             54
    4              4  A002  R051  02-00-00  05-01-11  16:00:00  REGULAR   3144594   1088275              170             44
    5              5  A002  R051  02-00-00  05-01-11  20:00:00  REGULAR   3144808   1088317              214             42
    6              6  A002  R051  02-00-00  05-02-11  00:00:00  REGULAR   3144895   1088328               87             11
    7              7  A002  R051  02-00-00  05-02-11  04:00:00  REGULAR   3144905   1088331               10              3
    8              8  A002  R051  02-00-00  05-02-11  08:00:00  REGULAR   3144941   1088420               36             89
    9              9  A002  R051  02-00-00  05-02-11  12:00:00  REGULAR   3145094   1088753              153            333
    '''
    
    df['temp'] = df.EXITSn.shift(1)
    df['EXITSn_hourly'] = (df['EXITSn'] - df['temp'])
    del df['temp']
    df['EXITSn_hourly'].fillna(0, inplace=True)
    return df

#df = get_hourly_exits(df)
#print df.head()

## Question 2.10

#time = df['TIMEn'][0]


def time_to_hour(time):
    '''
    Given an input variable time that represents time in the format of:
    00:00:00 (hour:minutes:seconds)
    
    Write a function to extract the hour part from the input variable time
    and return it as an integer. For example:
        1) if hour is 00, your code should return 0
        2) if hour is 01, your code should return 1
        3) if hour is 21, your code should return 21
        
    Please return hour as an integer.
    '''
    
    hour = int(time[:2])
    return hour
    
#print "Time:", time_to_hour(time)


## Question 2.11
import datetime

#date = df['DATEn'][0]

def reformat_subway_dates(date):
    '''
    The dates in our subway data are formatted in the format month-day-year.
    The dates in our weather underground data are formatted year-month-day.
    
    In order to join these two data sets together, we'll want the dates formatted
    the same way.  Write a function that takes as its input a date in the MTA Subway
    data format, and returns a date in the weather underground format.
    
    Hint: 
    There is a useful function in the datetime library called strptime. 
    More info can be seen here:
    http://docs.python.org/2/library/datetime.html#datetime.datetime.strptime
    '''

    date_formatted = datetime.datetime.strptime(date, "%m-%d-%y").strftime("%Y-%m-%d")
    return date_formatted

#print "Old format: ", date
#print "New format: ", reformat_subway_dates(date)

###################################################################

## Question 3.1
import numpy as np
import matplotlib.pyplot as plt

filename="..\\data\\turnstile_data_master_with_weather.csv"
weather_data = pd.read_csv(filename)

#print weather_data.head()

def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    plt.figure()
    
    turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].hist(bins=200, label="No rain").set_xlim([0, 6000]) # your code here to plot a historgram for hourly entries when it is not raining
    turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].hist(bins=200, label="Rain").set_xlim([0, 6000]) # your code here to plot a historgram for hourly entries when it is raining
    plt.legend()
    return plt

#print entries_histogram(weather_data)

## Question 3.2
## If we had a small sample size, we could not use Welch's T test, 
## but since we have a sufficiently large enough sample size;
## we can use it although the Mann-Whitney would help bolster our claims 
## since it is a non-parametric test used for non-normal distribution comparisons.

## Question 3.3
import scipy
import scipy.stats

def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    
    You will want to take the means and run the Mann Whitney U-test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    
    You should feel free to use scipy's Mann-Whitney implementation, and you 
    might also find it useful to use numpy's mean function.
    
    Here are the functions' documentation:
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    
    You can look at the final turnstile weather data at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    with_rain = turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].reset_index(drop=True)
    without_rain = turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].reset_index(drop=True)
    U, p = scipy.stats.mannwhitneyu(without_rain, with_rain)
     
    return without_rain.mean(),with_rain.mean(), U, p # Grader output for means are reversed compared to instructions


# print mann_whitney_plus_means(weather_data)

## Question 3.4
## I ran the Mann-Whiteney U-test and \
## got a difference with (p = 0.019) chance of the difference being due to chance; \
## the result is statistically significant.
## We can reject the  null hypothesis that two populations are the same.

## Question 3.5

import pandas
from ggplot import *

"""
In this question, you need to:
1) implement the compute_cost() and gradient_descent() procedures
2) Select features (in the predictions procedure) and make predictions.

"""

def normalize_features(array):
   """
   Normalize the features in the data set.
   """
   mu = array.mean()
   sigma = array.std()
   array_normalized = (array - mu)/ sigma


   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, 
    and the values for our thetas.
    
    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """
    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    
    This can be the same gradient descent code as in the lesson #3 exercises,
    but feel free to implement your own.
    """
    
    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        cost_history.append(compute_cost(features, values, theta))
        theta = theta + (alpha/m)* np.dot((values - np.dot(features, theta)), features)
    
    return theta, pandas.Series(cost_history)

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.20 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~15%) of the data contained in 
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with 
    this computer on your own computer, locally. 
    
    
    If you'd like to view a plot of your cost history, uncomment the call to 
    plot_cost_history below. The slowdown from plotting is significant, so if you 
    are timing out, the first thing to do is to comment out the plot command again.
    
    If you receive a "server has encountered an error" message, that means you are 
    hitting the 30-second limit that's placed on running your program. Try using a 
    smaller number for num_iterations if that's the case.
    
    If you are using your own algorithm/models, see if you can optimize your code so 
    that it runs faster.
    '''
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
    
    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    
    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # Set values for alpha, number of iterations.
    alpha = 0.2 # please feel free to change this value
    num_iterations = 15 # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array, 
                                                            values_array, 
                                                            theta_gradient_descent, 
                                                            alpha, 
                                                            num_iterations)
    
    plot = None
    # -------------------------------------------------
    # Uncomment the next line to see your cost history
    # -------------------------------------------------
    plot = plot_cost_history(alpha, cost_history)
    # 
    # Please note, there is a possibility that plotting
    # this in addition to your calculation will exceed 
    # the 30 second limit on the compute servers.
    
    predictions = np.dot(features_array, theta_gradient_descent)
    return predictions, plot


def plot_cost_history(alpha, cost_history):
   """This function is for viewing the plot of your cost history.
   You can run it by uncommenting this

       plot_cost_history(alpha, cost_history) 

   call in predictions.
   
   If you want to run this locally, you should print the return value
   from this function.
   """
   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
      geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )


filename="..\\data\\turnstile_data_master_with_weather.csv"
weather_data = pd.read_csv(filename)

#preds, plot1 = predictions(weather_data)
#print preds
#print plot1

## Question 3.6

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    
    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins = 100)
    return plt
    
#print plot_residuals(weather_data, preds)

## Question 3.7

import sys

def compute_r_squared(data, predictions):
    '''
    In exercise 5, we calculated the R^2 value for you. But why don't you try and
    and calculate the R^2 value yourself.
    
    Given a list of original data points, and also a list of predicted data points,
    write a function that will compute and return the coefficient of determination (R^2)
    for this data.  numpy.mean() and numpy.sum() might both be useful here, but
    not necessary.

    Documentation about numpy.mean() and numpy.sum() below:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
    '''
    
    r_squared = 1 - np.sum(np.square(data - predictions)) / np.sum(np.square(data - np.mean(data)))
    #r_squared = 1 - np.square(data - predictions).sum() / np.square(data - np.mean(data)).sum()
    
    return r_squared

#print "R^2: ", compute_r_squared(weather_data['ENTRIESn_hourly'], preds)

## Question 3.8
import statsmodels.formula.api as smf

"""
In this optional exercise, you should complete the function called 
predictions(turnstile_weather). This function takes in our pandas 
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.  

In exercise 3.5 we used Gradient Descent in order to compute the coefficients
theta used for the ridership prediction. Here you should attempt to implement 
another way of computing the coeffcients theta. You may also try using a reference implementation such as: 
http://statsmodels.sourceforge.net/devel/generated/statsmodels.regression.linear_model.OLS.html

One of the advantages of the statsmodels implementation is that it gives you
easy access to the values of the coefficients theta. This can help you infer relationships 
between variables in the dataset.

You may also experiment with polynomial terms as part of the input variables.  

The following links might be useful: 
http://en.wikipedia.org/wiki/Ordinary_least_squares
http://en.wikipedia.org/w/index.php?title=Linear_least_squares_(mathematics)
http://en.wikipedia.org/wiki/Polynomial_regression

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent computed in Exercise 3.5?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~10%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting 
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""

def predictions(weather_turnstile):
 
    #print weather_turnstile
    #unit_groups = weather_turnstile.groupby(['UNIT'])
    #weather_turnstile['popularity'] = unit_groups[['ENTRIESn_hourly']].transform(sum).sort('ENTRIESn_hourly', ascending=False)
    ## Not used in exercise problem. Hour here is 0-23 and much less predictive than hour in the version 2 of the dataset.
    model = smf.ols(formula="ENTRIESn_hourly ~ UNIT + C(Hour)", data=weather_turnstile)

    results = model.fit()
    predictions = results.predict()
    #print predictions
    #print results.summary()
    return predictions 
    
    
#pred2 = predictions(weather_data)

## Question 4.1/4.2

from pandas import *


def plot_weather_data(turnstile_weather):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in Project 3.
    
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out the link 
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather 
    dataframe.
     
    However, due to the limitation of our Amazon EC2 server, we will give you only 
    about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    
    ## The server encountered an error. Please try running again. encountered a lot.
    ## ggplot missing many features. Only basic plots shown for inbrowser exercises.
    
    ## Q4.1    
    plot = ggplot(turnstile_weather, aes('ENTRIESn_hourly', fill='rain')) + geom_bar(binwidth=100) + xlim(low=0, high=5000) + \
    xlab("Hourly Entries - Bins of Size 100") + \
    ylab("Hourly Entries - Count in each bin") + \
    ggtitle("Hourly Entries Histogram - Rain vs. No Rain (Stacked)")
    ## Q. 4.2
    plot2 = ggplot(weather_data, aes('Hour', 'ENTRIESn_hourly', fill='rain')) + geom_bar() + \
        xlab("Hour of the day") + ggtitle("Distribution of ridership throughout the day - Rain (Blue) / No Rain (Red)") + ylab("Entries")    
    
    return plot, plot2
    
#print plot_weather_data(weather_data)


