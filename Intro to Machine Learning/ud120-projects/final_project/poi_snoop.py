# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:14:20 2015

@author: fch

Library for testing alternative sub-optimal feature selection procedures.

This module tests alternative sub-optimal feature selection procedures to 
provide example optimistic metrics as part of the Udacity Data Analyst
 Nanodegree Program.

Available functions include:
- get_top_features_all_data: Give an estimate of the model produced by 
    grid_search using features selected from using ExtraTreesClassifier 
    on the entire dataset before searching for a model.

"""
from poi_add_features import top_importances
from tester import test_classifier
from feature_format import featureFormat, targetFeatureSplit
from poi_data import features_split_pandas, combine_to_dict

def get_top_features_all_data(X_df, y_df, grid_searcher, top_N=9):
    '''Give an estimate of the model produced by grid_search using features
        selected from using ExtraTreesClassifier on the entire dataset before
        searching for a model.
        
    In general, this may produce overly optimistic results since there is 
        leakage from the test dataset when selecting features using the entire
        dataset.
        This is to show that this can improve cross-validated internal testing
        over choosing kbest within each cross-validation fold, but is still
        overly optimistic if the model were to be used on completely new data.
        
    Args:
        X_df: Pandas dataframe of features used to predict.
        y_df: Pandas dataframe of labels being predicted.
        grid_searcher: GridSearchCV object being searched over for optimal 
            tuning parameters.
        top_N: Top N features to retain based on feature importances obtained
            from the ExtraTreesClassifier estimator used in the
            top_N_features() function.
    Returns:
        A list of the top N features that were selected to be fed into the
        GridSearchCV object.
    
    Prints:
        Test results from the 1000 cross-validation splits testing in tester.py
        
    '''
    top_N_features = top_importances(X_df, y_df, top_N=top_N)
    top_N_names = list(top_N_features.index)
    X_df = X_df[top_N_names]
    features_list = ['poi'] + list(top_N_names)
    grid_searcher.fit(X_df, y_df)
    clf = grid_searcher.best_estimator_
    my_dataset = combine_to_dict(features_df=X_df, labels_df=y_df)
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    test_classifier(clf, my_dataset, features_list)
    return top_N_features
