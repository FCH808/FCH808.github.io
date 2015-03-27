#!/usr/bin/python


"""
    starter code for the validation mini-project
    the first step toward building your POI identifier!

    start by loading/formatting the data

    after that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../ud120-projects/tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../ud120-projects/final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

### Splitting train/test

from sklearn.cross_validation import train_test_split

train_features, test_features, train_labels, test_labels = train_test_split(features, labels,
                                                                            test_size=0.3,
                                                                            random_state=42)

### Train decision tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

clf = DecisionTreeClassifier()
clf.fit(train_features, train_labels)

pred = clf.predict(test_features)

print "Confusion Matrix:\n", confusion_matrix(test_labels, pred), "\n"
print "Classification Report:\n", classification_report(test_labels, pred)
print "Accuracy:", accuracy_score(test_labels, pred)