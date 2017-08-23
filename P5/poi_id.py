#!/usr/bin/python

import sys
import pickle
import pandas as pd
import numpy as np
import operator
sys.path.append("../tools/")

from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import MinMaxScaler
from feature_format import featureFormat, targetFeatureSplit
from sklearn import cross_validation
from sklearn.decomposition import PCA
from sklearn.metrics import precision_score, recall_score, f1_score


def compute_poi_communication_index(from_this_person_to_poi, from_poi_to_this_person, from_messages, to_messages):

    """ returns a number between 0 and 1 that represents the amount of communication between a person and a poi
        by multiplying the percentage of mail send to and received from a poi compared to the total mail send and
        received by a person.
   """

    if (from_this_person_to_poi == 0) or (from_poi_to_this_person == 0):
        from_poi_perc = 0.
    else:
        from_poi_perc = float(from_this_person_to_poi) / float(from_messages)

    if (from_messages == 0) or (to_messages == 0):
        to_poi_perc = 0.
    else:
        to_poi_perc = float(from_poi_to_this_person) / float(to_messages)

    from_to_add = from_poi_perc + to_poi_perc
    from_to_mlt = from_poi_perc * to_poi_perc

    return from_poi_perc, to_poi_perc, from_to_add, from_to_mlt

def clf_fit_and_evaluate(clf, features, labels, pca_on, print_it, iters):

    ### run the evaluation 200 times and take the average scores, because every unique evaluation gives an unique score

    prec_poi, prec_non_poi, rec_poi, rec_non_poi, f1_poi, f1_non_poi = 0, 0, 0, 0, 0, 0

    divider = iters
    
    for iter in range (iters):

        ### split the data in 30% test data and 70% training data, no random state to get different results every split
        training_features, testing_features, training_labels, testing_labels = \
            cross_validation.train_test_split(features, labels, test_size=0.33)

        ### if principal component analysis is used, train and test data must be converted before fitting

        if pca_on:
            pca = PCA(n_components = 5)
            pca.fit(training_features)
            training_features = pca.transform(training_features)
            testing_features = pca.transform(testing_features)

        ### fit classifier, predict and determine precision, recall and f1
        clf.fit(training_features, training_labels)
        pred = clf.predict(testing_features)
        precision = precision_score(testing_labels, pred, average=None)
        # when scoring fails, ignore it
        try:
            prec_poi+=precision[1]
            prec_non_poi+=precision[0]       
            recall = recall_score(testing_labels, pred, average=None)
            rec_poi += recall[1]
            rec_non_poi += recall[0]
            f1 = f1_score(testing_labels, pred, average=None)
            f1_poi += f1[1]
            f1_non_poi += f1[0]
        except:
            divider-=1


    prec_poi/=divider
    prec_non_poi/=divider
    rec_poi/=divider
    rec_non_poi/=divider
    f1_poi/=divider
    f1_non_poi/=divider
    if print_it:
        print 'precision poi      : ', round(prec_poi, 2)
        print 'precision non-poi  : ', round(prec_non_poi, 2)
        print 'recall poi         : ', round(rec_poi, 2)
        print 'recall non-poi     : ', round(rec_non_poi, 2)
        print 'f1 poi             : ', round(f1_poi, 2)
        print 'f1 non-poi         : ', round(f1_non_poi, 2)


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'bonus', 'deferral_payments', 'deferred_income', 'director_fees',
              'exercised_stock_options', 'expenses', 'from_messages',
              'from_poi_to_this_person', 'from_this_person_to_poi', 'loan_advances',
              'long_term_incentive', 'other', 'restricted_stock', 'restricted_stock_deferred',
              'salary', 'shared_receipt_with_poi', 'to_messages', 'total_payments', 'total_stock_value']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### transfer data_dict to a dataframe for easy printing and getting info on shape and counts

df = pd.DataFrame(data_dict)
df = df.T
df = df.applymap(lambda x: pd.np.nan if x=='NaN' else x)

print 'Shape of dataframe           : ', df.shape
print 'POI values and count         : ', df['poi'].value_counts()
print 'Non-Nan values per feature   : ', df.count()

### Task 2: Remove outliers

for key in ('THE TRAVEL AGENCY IN THE PARK','TOTAL', 'LOCKHART EUGENE E'): data_dict.pop(key)

### Task 3: Create new feature(s)

# Perform feature selection
data = featureFormat(data_dict, features_list)
poi, features = targetFeatureSplit(data)

# Create additional features for each data point and add them to data_dict and features
added_features = []

keys = data_dict.keys()
ft_count = 0
for key in keys:

    ft = features[ft_count]

    f_poi_p, t_poi_p, f_t_add, f_t_mult = compute_poi_communication_index(ft[9], ft[8], ft[7], ft[17])

    added_feature = [f_poi_p, t_poi_p, f_t_add, f_t_mult]
    added_features.append(np.array(added_feature))
    data_dict[key]['from_poi_perc'] = f_poi_p
    data_dict[key]['to_poi_perc'] = t_poi_p
    data_dict[key]['from_to_add'] = f_t_add
    data_dict[key]['from_to_mult'] = f_t_mult

    ft_count+=1

add_features = np.array(added_features)

features = np.concatenate((features,add_features),axis=1)

# Rescale features
scaler = MinMaxScaler()
rescaled_features = scaler.fit_transform(features)

# Select 10 best features
selector = SelectKBest(score_func=f_classif, k=10)
selector.fit(features, poi)
is_best_features = selector.get_support()

#remove 'poi' from the predictor list and print sorted feature_scores
predictors = features_list + ['from_poi_perc', 'to_poi_perc', 'from_to_add', 'from_to_mult']
predictors.pop(0)

feature_scores = zip (predictors, selector.scores_)
feature_scores.sort(key = operator.itemgetter(1), reverse = True)
print "Feature scores "
for feature_score in feature_scores:
    print feature_score

### Store to my_dataset for easy export below.
my_dataset = data_dict

keys = data_dict.keys()
for key in keys:

    my_dataset[key].pop('email_address')
    for counter in range(23):

        if is_best_features[counter] == False:
            my_dataset[key].pop(predictors[counter])


### Extract features and labels from dataset for local testing

features_list = ['poi']
for counter in range(23):
    if is_best_features[counter] == True:
        features_list.append(predictors[counter])

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Rescale features after reloading best features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Create 5 classifiers with and without pca

for i in range (2):

    if i == 1:
        pca_on = False
        pca_text = ' without PCA'
    else:
        pca_on = True
        pca_text = ' with PCA'

    # classifier 1: Gaussian Naive Bayes
    from sklearn.naive_bayes import GaussianNB
    clf_gnb = GaussianNB()

    print ''
    print 'Gaussian Naive Bayes', pca_text
    clf_fit_and_evaluate(clf_gnb, features, labels, pca_on, True, 5000)

    # classifier 2: Decision Tree Classifier
    from sklearn import tree
    clf_dt = tree.DecisionTreeClassifier()

    print ' '
    print 'Decision Tree Classifier', pca_text
    clf_fit_and_evaluate(clf_dt, features, labels, pca_on, True, 5000)

    # classifier 3: Support Vector Machines
    from sklearn import svm
    clf_svm = svm.SVC(kernel="rbf")

    print ' '
    print 'Support Vector Machines', pca_text
    clf_fit_and_evaluate(clf_svm, features, labels, pca_on, True, 5000)

    # classifier 4: Logistic Regression
    from sklearn.linear_model import LogisticRegression
    clf_lr = LogisticRegression()

    print ''
    print 'Logistic Regression', pca_text
    clf_fit_and_evaluate(clf_lr, features, labels, pca_on, True, 5000)

    # classifier 5: KMeans
    from sklearn import cluster
    clf_km = cluster.KMeans(n_clusters=2)

    print ' '
    print 'KMeans', pca_text
    clf_fit_and_evaluate(clf_km, features, labels, pca_on, True, 5000)

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Choose KMeans without PCA as classifier to tune

from sklearn.grid_search import GridSearchCV
parameters = {'n_clusters': [1,2] , 'algorithm':('auto', 'full', 'elkan')
                , 'init':('k-means++', 'random'), 'n_init': [1,2,5,10,20]}
from sklearn import cluster
km = cluster.KMeans()
clf = GridSearchCV(km, parameters)
clf.fit(features, labels)
print 'best params: ', clf.best_params_
print 'best estimator: ', clf.best_estimator_

print ' '
print 'Tuned k-nearest Neigbours'
clf_fit_and_evaluate(clf, features, labels, False, True, 200)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

# Winner: Gaussian Naive Bayes with PCA
clf = GaussianNB()
clf_fit_and_evaluate(clf, features, labels, True, False, 5000)

dump_classifier_and_data(clf, my_dataset, features_list)