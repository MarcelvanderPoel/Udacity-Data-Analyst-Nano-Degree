# Project Identify Fraud from Enron Email

## Project Overview

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. In this project, I built a person of interest (POI) identifier based on financial and email data made public as a result of the Enron scandal. This data was combined with a hand-generated list of POI in the fraud case.

## Project question and dataset 

##### Goal of the project
The goal of the project is to determine who is a POI based on financial and email data made public.
Machine learning in this case can be useful by classifying persons based on the financial and email data into a POI group and a non-POI group.
For this purpose, POI were identified based on the fact if they were indicted, reached a settlement or plea deal or testified in exchange for prosecution immunity

The dataset provided contains 146 datapoints and 21 features (14 financial, 6 email and 1 POI feature).
From the 146 datapoints, 18 are marked as POI and 128 are marked as non-POI.
Not all datapoints have values for every feature:


</div>
<table class="tg">
  <tr>
    <th class="tg-9hbo">Feature</th>
    <th class="tg-amwm">Count</th>
  </tr>
  <tr>
    <td class="tg-yw4l">bonus</td>
    <td class="tg-baqh">82</td>
  </tr>
  <tr>
    <td class="tg-yw4l">deferral_payments</td>
    <td class="tg-baqh">39</td>
  </tr>
  <tr>
    <td class="tg-yw4l">deferred_income</td>
    <td class="tg-baqh">49</td>
  </tr>
  <tr>
    <td class="tg-yw4l">director_fees</td>
    <td class="tg-baqh">17</td>
  </tr>
  <tr>
    <td class="tg-yw4l">email_address</td>
    <td class="tg-baqh">11</td>
  </tr>
  <tr>
    <td class="tg-yw4l">exercised_stock_options</td>
    <td class="tg-baqh">102</td>
  </tr>
  <tr>
    <td class="tg-yw4l">expenses</td>
    <td class="tg-baqh">95</td>
  </tr>
  <tr>
    <td class="tg-yw4l">from_messages</td>
    <td class="tg-baqh">86</td>
  </tr>
  <tr>
    <td class="tg-yw4l">from_poi_to_this_person</td>
    <td class="tg-baqh">86</td>
  </tr>
  <tr>
    <td class="tg-yw4l">from_this_person_to_poi</td>
    <td class="tg-baqh">86</td>
  </tr>
  <tr>
    <td class="tg-yw4l">loan_advances</td>
    <td class="tg-baqh">4</td>
  </tr>
  <tr>
    <td class="tg-yw4l">long_term_incentive</td>
    <td class="tg-baqh">66</td>
  </tr>
  <tr>
    <td class="tg-yw4l">other</td>
    <td class="tg-baqh">93</td>
  </tr>
  <tr>
    <td class="tg-yw4l">poi</td>
    <td class="tg-baqh">146</td>
  </tr>
  <tr>
    <td class="tg-yw4l">restricted_stock</td>
    <td class="tg-baqh">110</td>
  </tr>
  <tr>
    <td class="tg-yw4l">restricted_stock_deferred</td>
    <td class="tg-baqh">18</td>
  </tr>
  <tr>
    <td class="tg-yw4l">salary</td>
    <td class="tg-baqh">95</td>
  </tr>
  <tr>
    <td class="tg-yw4l">shared_receipt_with_poi</td>
    <td class="tg-baqh">86</td>
  </tr>
  <tr>
    <td class="tg-yw4l">to_messages</td>
    <td class="tg-baqh">86</td>
  </tr>
  <tr>
    <td class="tg-yw4l">total_payments</td>
    <td class="tg-baqh">125</td>
  </tr>
  <tr>
    <td class="tg-yw4l">total_stock_value</td>
    <td class="tg-baqh">126</td>
  </tr>
</table>
</div>


## Features

While exploring the dataset I noticed the following:
1) Two odd POI, namely 'THE TRAVEL AGENCY IN THE PARK' with only a value for the features other and total, and 'TOTAL' 
with very high values (outliers) from which i assume it is the total of all data points. Since these don't represent
persons, I removed them from the dataset. 
2) LOCKHART EUGENE E is the only person with NaN values for all features. I removed him from the dataset.

I made the assumption that POI share fraud related information more between themselves then with non-POI and that this
could show through the relative portion of mail they send and receive from other POI. For this I created four additional
features, the percentage of mail received from POI, send to POI and these two percentages added and multiplied.

I used SelectKBest to select the 10 most powerful features for classifying after rescaling them with the MinMax rescaler.
Based on these 10 I fitted and compared all the machine learning algorithms and choose the best performing Gaussian
Naive Bayes. With GNB I then compared all possible values for k for SelectKBest and found out that the 5 strongest 
features gave the best results. None of the new features were in this top 5:

<table class="tg">
  <tr>
    <th class="tg-yw4l">result SelectKBest</th>
    <th class="tg-yw4l">score</th>
  </tr>
  <tr>
    <td>exercised_stock_options</td>
    <td>24.82</td>
  </tr>
  <tr>
    <td>total_stock_value</td>
    <td>24.18</td>
  </tr>
  <tr>
    <td>bonus</td>
    <td>20.79</td>
  </tr>
  <tr>
    <td>salary</td>
    <td>18.29</td>
  </tr>
   <tr>
    <td>deferred_income</td>
    <td>11.46</td>
  </tr>
</table>

The four new features that I created came in place 10, 11, 12 and 22. The features on place 10, 11 and 12 were all
derived from the feature from_poi_to_this_person and all scored around the same. Using these features didn't lead 
to a better accuracy, precision or recall when fitting with Gaussian Naive Bayes. Using the best performing new feature
(from_po_perc) resulted in an f1 score of 0.3029. Using only the five best scoring features resulted in an f1 score of 
0.38696.

## Picking an algorithm

I looked at the following classification algorithms, with and without PCA. Principal component analysis is used on all these algorithms to reduce the dimensionality of the input features.

<TABLE BORDER=0>
<TR>
<TD>
<table>
  <tr>
    <th>Gaussian Naive Bayes  with PCA</th>
    <th></th>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.84757</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.45059</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.3055</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.36412</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Decision Tree Classifier  with PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.78664</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.23652</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.2215</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.22876</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Support Vector Machines  with PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.851</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.10185</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.0055</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.01044</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Logistic Regression  with PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.86264</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.63322</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.0915</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.1599</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>KMeans  with PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.58079</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.1621</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.464</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.24026</td>
  </tr>
</table>
</TD>
<TD>
<table>
  <tr>
    <th>Gaussian Naive Bayes  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.85464</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.48876</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.3805</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.42789</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Decision Tree Classifier  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.79614</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.27967</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.271</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.27527</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Support Vector Machines  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.851</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.10185</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.0055</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.01044</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>Logistic Regression  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.86571</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.67857</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.114</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.19521</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <th>KMeans  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.5955</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.1614</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.4365</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.23566</td>
  </tr>
</table>  
</TD>
</TR>
</TABLE>                

Gaussian Naive Bayes, with and without PCA, is the only algorithm that scores more than 0.3 for both recall and
precision.

Gaussian Naive Bayes is a simple algorithm that can't be tuned, I therefore tried to see if tuning the second best, 
decision tree, would result in better scores.

## Tuning an algorithm

Parameter tuning in machine learning is the process of optimizing parameter settings for a learning algorithm.
Tuning your algorithm allows you to get the best possible results and can help avoid overfitting.

I used GridSearchCV with the following parameters to tune DecisionTreeClassifier: 
{'criterion': ('gini', 'entropy') , 'splitter':('best', 'random'), 'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15],
    'min_samples_leaf': [1,2,3], 'max_features': [4,5,6,7,8,9,10]}.
                
The best estimator was DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
            max_features=5, max_leaf_nodes=None, min_impurity_split=1e-07,
            min_samples_leaf=3, min_samples_split=6,
            min_weight_fraction_leaf=0.0, presort=False, random_state=None,
            splitter='random')
     
Compared to Gaussian Naive Bayes the tuned DecisionTreeClassifier did not give better results for recall and precision.    

<TABLE BORDER=0>
<TR>
<TD>
<table>
  <tr>
    <th>Gaussian Naive Bayes  with PCA</th>
    <th></th>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.84757</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.45059</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.3055</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.36412</td>
  </tr>
</table>
</TD>
<TD> 
<table>
  <tr>
    <th>Gaussian Naive Bayes  without PCA</td>
    <td></td>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.85464</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.48876</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.3805</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.42789</td>
  </tr>
</table>  
</TD>
<TD> 
<table>
  <tr>
    <th>Tuned decision tree without pca</th>
    <th></th>
  </tr>
  <tr>
    <td>accuracy</td>
    <td>0.84114</td>
  </tr>
  <tr>
    <td>precision</td>
    <td>0.37665</td>
  </tr>
  <tr>
    <td>recall</td>
    <td>0.171</td>
  </tr>
  <tr>
    <td>f1</td>
    <td>0.23521</td>
  </tr>
</table>  
</TD>
</TR>
</TABLE>                


## Validation

Model validation in machine learning is the process where a trained model is evaluated with a testing data set, where 
training and testing data are separate portions of the same data set. We do this to make sure that the model has the
ability to be used to make predictions with a known reliability using other data sets.

I validated my results originally by splitting the data in 2/3 of training data and 1/3 of test data. To get better
metrics, I repeatedly fitted my classifiers and averaged the metrics over all the fits. But while doing this I did not
take into account that each fitting did not have approximately the same number of data points of POI and non-POI. 
I solved this by using the stratified shuffle split with the same settings as tester.py, to be able to compare the
results. This prevents imbalance in the distribution of the POI-indicator in the training and testing set. 

## Evaluation Metrics

Precision and recall were used as evaluation metrics. Recall is a metric that describes the number of true positives
in the population of true positives and false negatives combined (e.g. the percentage of POI identified correctly from 
all POI). Precision is a metric that describes the number of true positives in the population of true positives and 
false positives combined (e.g. the percentage of 'real' POI from all people identified as POI).
The f1-score is the harmonic mean of precision and recall. Gaussian Naive Bayes without PCA scores best on all metrics 
and is therefore the best algorithm for this project.

References:
1) Sklearn Documentation on http://scikit-learn.org
2) Udacity Course documentation
3) Stackoverflow website
4) Python documentation at https://docs.python.org
5) https://link.springer.com/referenceworkentry/10.1007%2F978-1-4419-9863-7_233
6) https://en.wikipedia.org/wiki/Hyperparameter_(machine_learning)
7) https://machinelearningmastery.com/how-to-improve-machine-learning-results/
8) https://books.google.nl/books?id=EwNwDQAAQBAJ&pg=PA108&lpg=PA108&dq=sklearn+pipeline+for+dummies+selectkbest&source=bl&ots=xz5q1AGmB-&sig=LpD1YHJq8CTxet58V4bV7uc6Wqs&hl=nl&sa=X&ved=0ahUKEwikmJqxovPVAhUIKlAKHRnQCg4Q6AEIajAI#v=onepage&q=sklearn%20pipeline%20for%20dummies%20selectkbest&f=false



I have cited above the origins of an parts of the submission that were taken from websites,
forums, blog posts, github repositories, etc.
