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
from wordcloud import WordCloud

stopWords = stopwords.words('english') + ['RT','rt'] + ['https']
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
        #for lines in tweets
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


def normalizeTup(tupledTweets,vectorizer):
    #print features
    tples = tupledTweets
   
    m = len(tples)
    tweets = []
  
    yValues = np.empty((m,))
    for i, line in enumerate(tples):
        yValues[i, ] = int(line[0].lower() == 'true')
        tweets.append(line[1])
        
    xValues = vectorizer.transform(tweets)
    
    
    return xValues, yValues
    
def createSparsMatrix(featureDict,tupledTweets, flag):
 
    #print features
    tples = tupledTweets
   
    m = len(tples)
    tweets = []
  
    yValues = np.empty((m,))
    for i, line in enumerate(tples):
        yValues[i, ] = int(line[0] == 'true')
        tweets.append(line[1])
        
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,3),max_features=10000)   
    if flag == 1:
        features = read_words(featureDict)
        vectorizer.fit(features)
    else:
        vectorizer.fit(featureDict)
    
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
    
def analyze_classifier(classifier,X_test,Y_test):
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
    

def predictSecond(xVals,yVals,classifier):
    
    print 'Classification report on training data with cross validation:'
    #break it up
    y_true = yVals
    y_pred =  classifier.predict(xVals)

    target_names = ['Not_Drug_Related', 'Drug_Related']
    print classification_report(y_true, y_pred, target_names=target_names)
    print
    #cm = confusion_matrix(y_true, y_pred)
    #print cm
    #plt.figure()
    #plot_confusion_matrix(cm,target_names)
    
    return xVals, y_pred
    
def  secondsetTrue(xValsTups,yVals,tupleList):
     
     #print(len(tupleList))
     #print(len(xValsTups))
     predictedTuples = []
     
     for i in range (len(yVals)):
         if yVals[i] == 1:
           
             tup = ('true',xValsTups[i][1])
             #print tup
             predictedTuples.append(tup)
     
     numTrues = len(predictedTuples)
     #print(numTrues)
     wantedNos = (len(yVals) - numTrues)/2
     #print(wantedNos)
     count = 0;
     for i in range(len(yVals)):
        if(yVals[i] == 0):
            count+=1
            tup = ('false',xValsTups[i][1])
            predictedTuples.append(tup)
        if count >= wantedNos:
            break;
     
     #print 'got here'
     #print len(predictedTuples)
     #print len(tupleList)
     
     
     combinedOldandNew = predictedTuples +tupleList
     
     features = []
     for i in combinedOldandNew:
         features.append(i[1])
     
     
    
     #print len(combinedOldandNew)
     return combinedOldandNew , features    
     
     
    
def tupleDrugTweets(tweetFile):
    tupledTweets = []
    count = 0
    with open(tweetFile,'r') as tweets:
        lines = tweets.readlines()
        for tweet in lines:
            try:
                if count < 100000:#200000:
                    tweet_object = json.loads(tweet.rstrip(),strict=False)
                    msg = tweet_object['text']
                    
                    try:
                        words = [i.strip('.,*;-:"\'`?!)(').lower() for i in msg.split() if i.strip('.,*;-:"\'`?!)(').lower() not in stopWords]
                        newString = ""
                        for w in words:
                            newString += " "+w.encode('utf-8')
                      
                        #all tweets will be false by default 
                        #to many tweets to label this is for word cloud
                        tup = ('true',str(newString.strip()))
                        tupledTweets.append(tup)
                        count += 1
                        #print json_data
                    except: 
                        continue
                
            except ValueError, e:
                print e
    return tupledTweets    
    

    



def trainClassifierA():
    File  = "./Json/handJson2.json"
    buildFeatureList(File)
    tupleList = buildFeatureObject(File)
    
    xVals, yVals, vectorizer = createSparsMatrix(featureDictionary ,tupleList,1) 
    
    #save vectorizer    
    #joblib.dump(vectorizer, 'vectorizer.pkl')
    
    #Split data between test and training
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(xVals, yVals, test_size=0.2, random_state=5)
    
    
    
    # scoring = 'roc_auc', 'precision'
    scoring = 'f1'
    
    classifier = train_classifier(X_train,Y_train,scoring)
    
    
    #save classifier
    #joblib.dump(classifier, 'amt_1_' + scoring + '_SVC_.pkl')
    
    #test Classifier A
    xVals, yVals = predictSecond(X_test,Y_test,classifier)
    
    #analyze classfier A
    analyze_classifier(classifier, X_test, Y_test)
    
    return classifier

def trainClassifierB():
    File  = "./Json/handJson2.json"
    buildFeatureList(File)
    tupleList = buildFeatureObject(File)
    secondDataSet  = './Json/finalData.json'
    
    #tuple of tweets preocssed and drug relation boolean
    tupledTweetsSecond =  buildFeatureObject(secondDataSet)
    
    
    #joblib.dump(tupledTweetsSecond, 'tupleSecondData.pkl')
    
    #tupledTweetsSecond = joblib.load('tupleSecondData.pkl')

    #load vectorizer of classifier A
    vectorizer = joblib.load('vectorizer.pkl')
    
    #turn the tweets into xVals and Y Vals
    xVal2nd, yVals2nd = normalizeTup(tupledTweetsSecond,vectorizer)

    #load classifier A 
    classifier = joblib.load('amt_1_f1_SVC_.pkl')
    
    #predict the labels of 2nd data set
    xvals, yvalsPred = predictSecond(xVal2nd,yVals2nd,classifier)
  
    
    #Take all the trues half of the falses predicted
    #combine with all tweets of all data set 1.
    finalTuple, features= secondsetTrue(tupledTweetsSecond,yvalsPred,tupleList)
       
    #begin bootstrapping a new classifier
    allXs, allYs, secondVectorizer = createSparsMatrix(features,finalTuple,2)

    #joblib.dump(secondVectorizer,'vectorizer_2.pkl')
    

    #split training and test
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(allXs, allYs, test_size=0.2, random_state=5)
    
    scoring = 'f1'
    #train new classifier
    classifier_two = train_classifier(X_train,Y_train,scoring)
    
    #save classifier
    joblib.dump(classifier_two, 'classifierB.pkl')
    
    #load classifier B
    #classifier_two = joblib.load('amt_2_f1_SVC_.pkl')
    
    #anaylyze preformance
    #analyze_classifier(classifier_two, X_test,Y_test)
    #xvals, yvalsPred = predictSecond(X_test, Y_test,classifier_two)
    
    return classifier_two
    
    
def generateWordCloud():
    
    drugTweetsFile = './Json/Drug_Tweets4_14.json'
    
    tupleDrugsJson = tupleDrugTweets(drugTweetsFile)
    
    print(len(tupleDrugsJson))
    
    #load Classifier B's Vectorizer 
    vectorizer = joblib.load('vectorizer_2.pkl')
    
    xValues, yValues = normalizeTup(tupleDrugsJson,vectorizer)
   
    #load classiferB 
    classifier = joblib.load('classifierB.pkl')
    
    wordList = []
    
    xValues, y_pred  = predictSecond(xValues,yValues,classifier)
 
    for  i  in range(0,len(y_pred)):
        if( y_pred[i] == 1):
            s = set()
            for word in vectorizer.inverse_transform(xValues[i]):
                for w in word:
                    words = w.split()
                    for aWord in words:
                        if aWord not in stopWords:
                            s.add(aWord.encode("utf-8"))
            wordList.extend(list(s))
   
    
    #print wordList
    
    text = " " .join(wordList)
    #print text
    
    wordcloud = WordCloud(max_font_size=40, width=800, height=400,max_words=500).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
def rankLexicon():
    
    filterList = [r'\\x','https']
    vectorizer = joblib.load('vectorizer_2.pkl')    
    #classifier = joblib.load('classifierB.pkl')
    featureList = []
    for i in vectorizer.get_feature_names(): 
        for item in filterList:
            if(item in i.encode("utf-8") ):
                break;
        featureList.append(i.encode("utf-8"))
    print featureList

def topVectors():
    classifier = joblib.load('classifierB.pkl')
    print classifier





def main():
    #A = trainClassifierA()
    #B = trainClassifierB()
    
    #generateWordCloud()
    
    #rankLexicon()
    topVectors()
    
if __name__ == "__main__":
	main() 
