#!/usr/bin/python

import os
import pickle
import re
import sys
from nltk.stem.snowball import SnowballStemmer

sys.path.append( "../ud120-projects/tools/" )
from parse_out_email_text import parseOutText

"""
    starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification

    the list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    the actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project

    the data is stored in lists and packed away in pickle files at the end

"""


from_sara  = open("../ud120-projects/text_learning/from_sara.txt", "r")
from_chris = open("../ud120-projects/text_learning/from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list
temp_counter = 0
text = ""

# sw = stopwords.words('english')

for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        ### only look at first 200 emails when developing
        ### once everything is working, remove this line to run over full dataset
        #temp_counter += 1
        #if temp_counter < 200:
            path = os.path.join('../ud120-projects/', path[:-1])
            #print path
            email = open(path, "r")
            ### use parseOutText to extract the text from the opened email
            text = parseOutText(email)
            # print text
            ### use str.replace() to remove any instances of the words
            remove_these = ["sara", "shackleton", "chris", "germani", "sshacklensf", "cgermannsf"]
            for word in remove_these:
                text = text.replace(word, "")
            
            # remove nltk stopwords:    
            # text = ' '.join([word for word in text.split() if word not in sw])
            
            ### append the text to word_data
            word_data.append(text)
            if name == 'sara':
                from_data.append(0)
            elif name == 'chris':
                from_data.append(1)
                
            #print word_data
            #print from_data
            ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
            email.close()

print "emails processed"
from_sara.close()
from_chris.close()

pickle.dump( word_data, open("../ud120-projects/text_learning/your_word_data.pkl", "w") )
pickle.dump( from_data, open("../ud120-projects/text_learning/your_email_authors.pkl", "w") )


### in Part 4, do TfIdf vectorization here
