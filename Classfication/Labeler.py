import json
import sys



def LabelTweets():
    #22-02-2015.json
    #Drug_Tweets4_14.json
    tweets_file = open('./Json/Drug_Tweets4_14.json','r')
    labeledTweets_file = open('./Json/DrugMoreData.json','a')
    #labeledTweets_file = open('./Json/RochesterTweetData.json','a')
    #labeledTweets_file = open('./Json/DetroitTweetData.json','a')
    unsure_tweets = open('./Json/UnsureTweets33.json','a')
    currentLine = 0
    leftOff = int(raw_input("What line would you like to start at? "))
    line = ""
    line = tweets_file.readline()
    while currentLine  < leftOff:
      line  = tweets_file.readline()
      currentLine+=1
      #print 'skipped'
    #print currentLine

    while line!= "":
        print ""

        #currentTweet = json.dumps(json.loads(line))
        currentTweet = json.loads(line)
        print currentTweet["text"].encode('utf-8')
        isDrugRelated =""
        while(1):
            print ""
            isDrugRelated = raw_input('Is this tweet drug related? t or f  or quit to exit ')
            if(isDrugRelated.lower() == 't'):
                drugRelated  = {'drug_relation':True}
                break;
            elif(isDrugRelated.lower() == 'f'):
                drugRelated  = {'drug_relation':False}
                break;
            elif(isDrugRelated.lower() == '?'):
                break;
            elif(isDrugRelated.lower() == 'quit'):
                print('Quiting...,CurrentLine to Label = ',currentLine)
                tweets_file.close()
                labeledTweets_file.close()
                return;
            elif(isDrugRelated.lower() == 'line'):
                print currentLine
                
        if(isDrugRelated.lower() == '?'):
            unsure_tweets.write(json.dumps(currentTweet)+"\n")
        else:
            currentTweet.update(drugRelated)
	    #print currentTweet
            labeledTweets_file.write(json.dumps(currentTweet)+"\n")
	    
        
        currentLine+=1
        #userInput = raw_input("Push Enter to conintue or type quit ")
        #if(userInput.lower() == 'quit'):
            #print( 'CurrentLine to Label = ',currentLine)
            #break;
        print ""
        line = tweets_file.readline()
        
 


def countTrue(jsonFile):
    labelDrugs = open(jsonFile,'r')
    line = labelDrugs.readline()
    counter = 0
    currentLine = 0
    while line != "":
        
        currentTweet = json.loads(line)
     
        
        if(currentTweet['drug_relation'] == True):
            counter += 1
        line = labelDrugs.readline()
        currentLine+=1
    print counter
    labelDrugs.close()
     

				
if __name__ == "__main__":
	#LabelTweets()
        countTrue('./Json/DrugMoreData.json')
