import json
import codecs


def searchDrugTweets():

		tweets_file = open('.\JsonFiles/BigJson/1year_filtered.json','r')
		tweet_keyword_file = open(".\JsonFiles\Drug_Keywords.json",'r')

		k = json.load(tweet_keyword_file)
		tweet_keyword_file.close()
		keys = set(k["key_words"])
		tags = set(k["hashtags"])

		keys.union(tags)

		flagged_users = set()

		count = 0
		file = open(".\TextFiles\Flagged_Drug_Tweets.txt","w")
		line = tweets_file.readline()
		while line != "":
				try:
						j = json.loads(line)
						tweet = set(j["text"].encode('unicode-escape').replace('\\',' ').lower().split())
						temp = keys.intersection(tweet)
						if temp:
								file.write(str(j["id"]))
								file.write(";")
								file.write(str(j["user"]["id_str"]))
								file.write(";")
								file.write(str(temp))
								file.write(";")
								file.write(str(j["created_at"])[5:25])
								file.write(";")
								file.write(str(j["text"].encode('unicode-escape')))
								file.write("\n")
								flagged_users.add(str(j["user"]["id_str"]))
								count = count + 1	
				except ValueError:
						pass
						file.write("\n")
				line = tweets_file.readline()	
		tweets_file.close()
		file.close()
				
		print "Number of Flagged Tweets:"	
		print count

		count = 0
		file = open(".\TextFiles\Flagged_Drug_Users.txt","w")
		for users in flagged_users:
				file.write(str(users))
				file.write("\n")
				count = count + 1
		file.close()

		print "Number of Flagged Users"
		print count
  
				
				
if __name__ == "__main__":
	searchDrugTweets()
	


