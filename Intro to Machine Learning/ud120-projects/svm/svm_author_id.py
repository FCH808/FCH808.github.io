#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 2 (SVM) mini-project

    use an SVM to identify emails from the Enron corpus by their authors
    
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../ud120-projects/tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()



#########################################################
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

if __name__ == '__main__':

    clt = SVC(kernel="linear")
    time0 = time()
    clt.fit(features_train, labels_train)
    print "Training time: ", round(time()-t0, 3), "seconds."
    
    t0 = time()
    pred = clt.predict(features_test)
    print "Prediction Time: ", round(time()-t0, 3), "seconds."
    
    acc = accuracy_score(pred, labels_test)
    print "Accuracy: ", acc
    
#########################################################

