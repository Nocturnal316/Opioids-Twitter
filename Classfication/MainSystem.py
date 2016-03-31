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
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer

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

   
def main():
    File  = "./Json/handJson.json"
    buildFeatureList(File)
    tpleList =  buildFeatureObject(File)
    createSparsMatrix(featureDictionary ,tpleList)    

if __name__ == "__main__":
	main() 
