# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 22:15:23 2016

@author: Nocturnal
"""

import pickle
import sys
import json
import unicodedata
import numpy as np
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report, precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
from sklearn import cross_validation, svm

stopWords = stopwords.words('english') + ['RT','rt']
featureDictionary =  "./Json/featueDict.txt"


def read_words(file_name):
    """
    Returns a list of lines read from the given file.
    """
    with open(file_name, 'r') as f:
        return f.readlines()

def buildFeatureList(tweetFile):
    """
        The file use to create the feature matrix
        each line containns text only per tweet with some procosssing done.
    """
    #wordsRemovedStop = set()
    with open(tweetFile,'r') as tweets, open(featureDictionary,'w') as writer:
        lines = tweets.readlines()
        for tweet in lines:
           try:
               tweet_object = json.loads(tweet.rstrip(),strict=False)
               msg = tweet_object['text']
               words = [i.strip('.,*;-:"\'`?!)(').lower() for i in msg.split() if i.strip('.,*;-:"\'`?!)(').lower() not in stopWords]
               processesSentence = ""
               for w in words:
                   #wordsRemovedStop.add(w.rstrip())
                   processesSentence +=" "+w.rstrip()
               
               writer.write(processesSentence.encode('utf-8') + '\n')
           except ValueError, e:
               print e
               return 0
  
#   with open(featureDictionary,'w') as writer:
#       for word in wordsRemovedStop:
#           writer.write(word.encode('utf-8') + '\n')


def buildFeatureObject(tweetFile):
    """
        format for keeping tweet and its Y values drug related or not
    """
    featureObjectFile = open("featureTweets.json",'a')
    tupledTweets = []
    with open(tweetFile,'r') as tweets:
        lines = tweets.readlines()
        for tweet in lines:
            try:
                tweet_object = json.loads(tweet.rstrip(),strict=False)
                msg = tweet_object['text']
              
                words = [i.strip('.,*;-:"\'`?!)(').lower() for i in msg.split() if i.strip('.,*;-:"\'`?!)(').lower() not in stopWords]
                data = {}
                newString = ""
                for w in words:
                    
                    newString += " "+w.encode('utf-8')
                    
                data['text'] = newString.strip()
                data['drug_relation'] = tweet_object['drug_relation']
                tup = (str(tweet_object['drug_relation']),str(newString.strip()))
                tupledTweets.append(tup)
                json_data = json.dumps(data)
                #print json_data
                featureObjectFile.write(json_data+'\n')
            except ValueError, e:
                print e
    featureObjectFile.close()
    return tupledTweets

def createSparsMatrix(featureDict,tupledTweets):
    features = read_words(featureDict)
    #print features
    tples = tupledTweets
   
    m = len(tples)
    tweets = []
  
    yValues = np.empty((m,))
    for i, line in enumerate(tples):
        yValues[i, ] = int(line[0] == 'true')
        tweets.append(line[1])
        
        
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,3),max_features=10000)
    vectorizer.fit(features)
    #print vectorizer.get_feature_names()
    xValues = vectorizer.transform(tweets)
    #print vectorizer.vocabulary_.get('high')
    #print xValues.toarray()
    return xValues, yValues, vectorizer

def train_classifier(X_train,Y_train,score):
    """
    Train 
    """
    
    weight_dicts = [{1:1, 0:1}, {1:5, 0:1}, {1:1, 0:5}, {1:10, 0:1}, {1:1, 0:10}, {1:20, 0:1}, {1:1, 0:20}]

    param_grid = [
    {'C':[0.01, 0.1, 1, 10, 100, 1000], 'kernel':['linear'], 'class_weight':weight_dicts, 'probability':[True, False], 'shrinking':[True, False]}
    ]
    
    classifier = GridSearchCV(svm.SVC(C=1), param_grid, cv=10, scoring=score)
    
    classifier.fit(X_train,Y_train)
    
    return classifier
 
def print_cv_classification_report(classifier, X_test, Y_test):
    """
    Prints weighted average of precision, recall and F1-score over each of the classes in the test dataset.
    
    see sklearn.metrics.classification_report
    """
    print 'Classification report on training data with cross validation:'
    y_true, y_pred = Y_test, classifier.predict(X_test)

    target_names = ['Not_Drug_Related', 'Drug_Related']
    print classification_report(y_true, y_pred, target_names=target_names)
    print
    cm = confusion_matrix(y_true, y_pred)
    print cm
    plt.figure()
    plot_confusion_matrix(cm,target_names)
    
def analyze_classifier(classifier,xVals,yVals,X_test,Y_test,vectorizer):
    """
    Analyzes the classifier.
    Input:
        clf - GridSearchCV instance
        X_test - test examples
        y_test - test labels
    """
    print_cv_classification_report(classifier, X_test, Y_test)
    
def plot_confusion_matrix(cm, target_names,title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    
    
def main():
    File  = "./Json/handJson2.json"
    buildFeatureList(File)
    tpleList =  buildFeatureObject(File)
    xVals, yVals, vectorizer = createSparsMatrix(featureDictionary ,tpleList)    
    
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(xVals, yVals, test_size=0.2, random_state=5)
    
    
    # scoring = 'roc_auc', 'precision'
    scoring = 'f1'
    
    classifier = train_classifier(X_train,Y_train,scoring)
    
    
    #joblib.dump(classifier, 'amt_1_' + scoring + '_SVC_.pkl')
    
    analyze_classifier(classifier, xVals, yVals, X_test, Y_test, vectorizer)

    
if __name__ == "__main__":
	main() 
