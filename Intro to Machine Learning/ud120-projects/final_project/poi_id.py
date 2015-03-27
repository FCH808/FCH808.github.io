#!/usr/bin/python
import pandas as pd
import sys
import pickle


sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from poi_model import *
from poi_add_features import *
from poi_data import *

pd.options.display.mpl_style = 'default'
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### Task 1.2: Fix out of sync records.
data_dict = fix_records(data_dict)

# Convert to pandas dataframe for the data shaping phase.
df = pd.DataFrame.from_dict(data_dict, orient='index')
# Remove email_address strings since they won't be used at all.
del df['email_address']

### Task 2: Remove outliers
df = remove_invalid_entries(df, invalid_name='TOTAL')

df = fill_zeros(df, include_inf=False)
### Task 3: Create new feature(s)

df = add_totals(df, email_data=False, financial_data=True)

###############################################################################
# Uncomment to add more features. Docstrings can be found in poi_add_features.py
# df = add_financial_ratios(df, to_payment=True, to_stock=False, to_total=True)
# df = add_email_ratios(df, to_message=False, from_messages=False,             #
#                     to_total=False, active_ratios=True)                     #
# df = fill_zeros(df, include_inf=True)                                        #
# df = add_squares(df, square_email=False, square_financial=True)              #
###############################################################################

### Store to my_dataset for easy export below.
# my_dataset = data_dict



### Task 4: Try a variety of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html



## __name__ must == '__main__' to run parallel processing/forking in Windows
if __name__ == "__main__":
    
    # Also removes any rows that have no entries at all. 
    # This includes only one records with no data, Eugene E. Lockhart
    X_df, y_df = features_split_pandas(df, remove_zeros_rows=True)

    X_features = list(X_df.columns)
    features_list = ['poi'] + X_features


    ### Task 5: Tune your classifier to achieve better than .3 precision and recall 
    ### using our testing script.
    ### Because of the small size of the dataset, the script uses stratified
    ### shuffle split cross validation. For more info: 
    ### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

    # StratifiedShuffleSplits for 1000 internal cross-validation splits
    # within the grid-search.
    sk_fold = StratifiedShuffleSplit(y_df, n_iter=1000, test_size=0.1)
    
    pipeline = get_LogReg_pipeline()
    params = get_LogReg_params(full_search_params=False)        
    
    #pipeline = get_LSVC_pipeline()
    #params = get_LSVC_params(full_search_params=False)
    
    #pipeline = get_SVC_pipeline()
    #params = get_SVC_params(full_search_params=False)
         
    # scoring_metric: average_precision, roc_auc, f1, recall, precision
    scoring_metric = 'recall'
    grid_searcher = GridSearchCV(pipeline, param_grid=params, cv=sk_fold,
                           n_jobs=-1, scoring=scoring_metric, verbose=0)
    ###########################################################################
    # Uncomment to see the tester.py cross-validated scores of the model      #
    # with the top 9 features selected from the entire dataset outside of     #
    # of the cross-validation loops. Also must import from poi_snoop.py                                        #
    # top_features_all = get_top_features_all_data(X_df, y_df, grid_searcher, top_N=9)    
    ###########################################################################
    grid_searcher.fit(X_df, y=y_df)
    
    mask = grid_searcher.best_estimator_.named_steps['selection'].get_support()
    top_features = [x for (x, boolean) in zip(X_features, mask) if boolean]
    n_pca_components = grid_searcher.best_estimator_.named_steps['reducer'].n_components_
    
    print "Cross-validated {0} score: {1}".format(scoring_metric, grid_searcher.best_score_)
    print "{0} features selected".format(len(top_features))
    print "Reduced to {0} PCA components".format(n_pca_components)
    ###################
    # Print the parameters used in the model selected from grid search
    print "Params: ", grid_searcher.best_params_ 
    ###################
    
    clf = grid_searcher.best_estimator_
    
    my_dataset = combine_to_dict(features_df=X_df, labels_df=y_df)
    ### Extract features and labels frouum dataset for local testing
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    
    test_classifier(clf, my_dataset, features_list)
    ### Dump your classifier, dataset, and features_list so 
    ### anyone can run/check your results.
    dump_classifier_and_data(clf, my_dataset, features_list)
