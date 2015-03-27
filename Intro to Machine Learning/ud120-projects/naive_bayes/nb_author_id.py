# Write the content of this cell as a python script.
# Using the same name, overwrite nb_author_id.py
# %%writefile nb_author_id.py

#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 1 (Naive Bayes) mini-project 

    use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../ud120-projects/tools/")
from email_preprocess import preprocess

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################

NB = GaussianNB()

t0 = time()
NB.fit(features_train, labels_train)
print "Training Time: ", round(time()-t0, 3), "seconds."

t0 = time()
pred = NB.predict(features_test)
print "Prediction Time: ", round(time()-t0, 3), "seconds."

accuracy = accuracy_score(pred, labels_test)

print "Accuracy: ", accuracy

#########################################################
