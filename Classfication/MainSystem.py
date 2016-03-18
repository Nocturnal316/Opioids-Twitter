# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 22:15:23 2016

@author: Nocturnal
"""


import sys
import json
import unicodedata
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
   wordsRemovedStop = set()

   with open(tweetFile,'r') as tweets:
       lines = tweets.readlines()
       for tweet in lines:
           try:
               tweet_object = json.loads(tweet.rstrip(),strict=False)
               msg = tweet_object['text']
               words = [i.strip('.,*;-:"\'`?!)(').lower() for i in msg.split() if i.strip('.,*;-:"\'`?!)(').lower() not in stopWords]
               for w in words:
                   wordsRemovedStop.add(w.rstrip())
               
           except ValueError, e:
               print e
               return 0
  
   with open(featureDictionary,'w') as writer:
       for word in wordsRemovedStop:
           writer.write(word.encode('utf-8') + '\n')


def buildFeatureObject(tweetFile):
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
                tup = (str(tweet_object['drug_relation']),str(newString.strip))
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
    
    for i, line in enumerate(tples):
        tweets.append(line[1])
        
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 4),max_features=10000)
    vectorizer.fit(features)
    print vectorizer.get_feature_names()
    xValues = vectorizer.transform(tweets)
    print xValues


   
def main():
    #buildFeatureList("./Json/handJson.json")
    tpleList =  buildFeatureObject("./Json/handJson.json")
    createSparsMatrix(featureDictionary ,tpleList)    

if __name__ == "__main__":
	main() 
