#!/usr/bin/python

import sys
import pickle
import pandas as pd
import numpy as np
import operator
sys.path.append("../tools/")

from tester                     import dump_classifier_and_data
from sklearn.feature_selection  import SelectKBest, f_classif
from sklearn.preprocessing      import MinMaxScaler
from feature_format             import featureFormat, targetFeatureSplit
from sklearn                    import cross_validation
from sklearn.cross_validation   import StratifiedShuffleSplit
from sklearn.decomposition      import PCA
from sklearn.metrics            import precision_score, recall_score, f1_score, classification_report
from sklearn.pipeline           import Pipeline


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


def test_classifier(clf, dataset, feature_list, pca_on, folds=1000):

    data = featureFormat(dataset, feature_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)
    scaler = MinMaxScaler()
    features = scaler.fit_transform(features)
    cv = StratifiedShuffleSplit(labels, folds, random_state=42)
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0
    for train_idx, test_idx in cv:
        features_train = []
        features_test = []
        labels_train = []
        labels_test = []
        for ii in train_idx:
            features_train.append(features[ii])
            labels_train.append(labels[ii])
        for jj in test_idx:
            features_test.append(features[jj])
            labels_test.append(labels[jj])

        ### if principal component analysis is used, train and test data must be converted before fitting

        if pca_on:
            pca = PCA(n_components = 5)
            pca.fit(features_train)
            features_train = pca.transform(features_train)
            features_test = pca.transform(features_test)

        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
            else:
                print "Warning: Found a predicted label not == 0 or 1."
                print "All predictions should take value 0 or 1."
                print "Evaluating performance for processed predictions:"
                break
    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0 * (true_positives + true_negatives) / total_predictions
        precision = 1.0 * true_positives / (true_positives + false_positives)
        recall = 1.0 * true_positives / (true_positives + false_negatives)
        f1 = 2.0 * true_positives / (2 * true_positives + false_positives + false_negatives)
        f2 = (1 + 2.0 * 2.0) * precision * recall / (4 * precision + recall)

        print 'accuracy  : ', round(accuracy, 5)
        print 'precision : ', round(precision, 5)
        print 'recall    : ', round(recall, 5)
        print 'f1        : ', round(f1, 5)
    except:
        print "Got a divide by zero when trying out:", clf
        print "Precision or recall may be undefined due to a lack of true positive predicitons."


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
print 'Features', data_dict
# Rescale features
scaler = MinMaxScaler()
rescaled_features = scaler.fit_transform(features)

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

print ''
print 'Determine best k for SelectKbest'
print ''

predictors = features_list + ['from_poi_perc', 'to_poi_perc', 'from_to_add', 'from_to_mult']

for num_of_features in range(1, 23):

    print 'Number of features: ', num_of_features

    pipeline = Pipeline(steps=[("sel", SelectKBest(k=num_of_features)),
                               ("clf", clf)])

    ### Get classifier score
    test_classifier(pipeline, data_dict, predictors, False)


# Select 5 best features
selector = SelectKBest(score_func=f_classif, k=5)
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
    test_classifier(clf_gnb, my_dataset, features_list, pca_on, folds=1000)

    # classifier 2: Decision Tree Classifier
    from sklearn import tree
    clf_dt = tree.DecisionTreeClassifier()

    print ' '
    print 'Decision Tree Classifier', pca_text
    test_classifier(clf_dt, my_dataset, features_list, pca_on, folds=1000)

    # classifier 3: Support Vector Machines
    from sklearn import svm
    clf_svm = svm.SVC(kernel="linear")

    print ' '
    print 'Support Vector Machines', pca_text
    test_classifier(clf_svm, my_dataset, features_list, pca_on, folds=1000)

    # classifier 4: Logistic Regression
    from sklearn.linear_model import LogisticRegression
    clf_lr = LogisticRegression()

    print ''
    print 'Logistic Regression', pca_text
    test_classifier(clf_lr, my_dataset, features_list, pca_on, folds=1000)

    # classifier 5: KMeans
    from sklearn import cluster
    clf_km = cluster.KMeans(n_clusters=2)

    print ' '
    print 'KMeans', pca_text
    test_classifier(clf_km, my_dataset, features_list, pca_on, folds=1000)

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Choose KMeans without PCA as classifier to tune

from sklearn.grid_search import GridSearchCV
parameters = {'criterion': ('gini', 'entropy') , 'splitter':('best', 'random')
                , 'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15], 'min_samples_leaf': [1,2,3]
                , 'max_features': [2,3,4,5]}

dt = tree.DecisionTreeClassifier()
clf = GridSearchCV(dt, parameters)
clf.fit(features, labels)
print 'best params: ', clf.best_params_
print 'best estimator: ', clf.best_estimator_

print ' '
print 'Tuned decision tree without pca'
test_classifier(clf, my_dataset, features_list, False, folds=1000)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

# Winner: Gaussian Naive Bayes with PCA
clf = GaussianNB()
pca_on=False
test_classifier(clf_gnb, my_dataset, features_list, pca_on, folds=1000)

dump_classifier_and_data(clf, my_dataset, features_list)