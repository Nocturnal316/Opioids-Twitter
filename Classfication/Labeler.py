import json
import sys



def LabelTweets():
    tweets_file = open('./Json/allTweets.json','r')
    labeledTweets_file = open('./Json/DrugLabeledTweets.json','a')
    currentLine = 0
    leftOff = int(raw_input("What line would you like to start at? "))
    line = ""
    line  = tweets_file.readline()
    while currentLine  < leftOff:
      line  = tweets_file.readline()
      currentLine+=1
      print 'skipped'
    print currentLine

    while line!= "":
        

        #currentTweet = json.dumps(json.loads(line))
        currentTweet = json.loads(line)
        print currentTweet["text"]
        isDrugRelated =""
        while(1):
            isDrugRelated = raw_input('is this tweet drug related? t or f  or quit to exit ')
            if(isDrugRelated.lower() == 't'):
                drugRelated  = {'drug_relation':'true'}
                break;
            elif(isDrugRelated.lower() == 'f'):
                drugRelated  = {'drug_relation':'false'}
                break;
            elif(isDrugRelated.lower() == 'quit'):
                print('Quiting...,CurrentLine to Label = ',currentLine)
                tweets_file.close()
                labeledTweets_file.close()
                return;
            
        
        
        currentTweet.update(drugRelated)
        #print currentTweet
        labeledTweets_file.write(json.dumps(currentTweet)+"\n")
        currentLine+=1
        #userInput = raw_input("Push Enter to conintue or type quit ")
        #if(userInput.lower() == 'quit'):
            #print( 'CurrentLine to Label = ',currentLine)
            #break;
        
        line = tweets_file.readline()
        
 









				
if __name__ == "__main__":
	LabelTweets()
