# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 22:15:23 2016

@author: Nocturnal
"""


import sys
import json
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer

stopWords = stopwords.words('english') + ['RT','rt']
featureDictionary =  "./Json/featueDict.txt"


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
                json_data = json.dumps(data)
                #print json_data
                featureObjectFile.write(json_data+'\n')
            except ValueError, e:
                print e
    featureObjectFile.close()

   
   
   
def main():
   buildFeatureObject("./Json/handJson.json")


if __name__ == "__main__":
	main() 
