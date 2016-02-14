# Filters tweets according to a list of words (word file: currently Oxycontin_Keywords.json)
# example use on the cycle3 server:

# nohup python -OO oxycontin_tweet_searcher_json.py /p/twitter4/rochester/*/*-*-*.json &> progress.txt &

import json
import codecs
import sys

def main():
    tweet_keyword_file = open("Oxycontin_Keywords.json")

    k = json.load(tweet_keyword_file)
    tweet_keyword_file.close()
    keys = set(k["key_words"])

    pain = set(k["pain"])
    killer = set(k["killer"])
    hills = set(k["hills"])
    heroin = set(k["heroin"])

    keys.union(killer)
    keys.union(hills)

    #oxy_tweets = set()
    #double_tweets = set()
    flagged_users = set()

    count = 0
    file = open("Flagged_Oxycontin_Tweets_Filtered.json","w")

    iterargs = iter(sys.argv)
    next(iterargs)
    for x in iterargs:
        tweets_file = open(x)

        line = tweets_file.readline()
        while line != "":
            try:
                j = json.loads(line.lower())
                #if j["id"] not in oxy_tweets:
                tweet = set(j["text"].encode('unicode-escape').replace('\\',' ').replace('#',' ').split())
                temp = keys.intersection(tweet)
                if temp:
                    kill = killer.intersection(temp)
                    hillbill = hills.intersection(temp)
                    if kill:
                        p = pain.intersection(tweet)
                        if p:
                            file.write(line)
                            #file.write("\n")
                            #oxy_tweets.add(j["id"])
                            flagged_users.add(str(j["user"]["id_str"]))
                            count = count + 1
                    elif hillbill:
                        h = heroin.intersection(temp)
                        if h:
                            file.write(line)
                            #file.write("\n")
                            #oxy_tweets.add(j["id"])
                            flagged_users.add(str(j["user"]["id_str"]))
                            count = count + 1
                    else:
                        file.write(line)
                        #file.write("\n")
                        #oxy_tweets.add(j["id"])
                        flagged_users.add(str(j["user"]["id_str"]))
                        count = count + 1
                # else:
                # 	double_tweets.add(j["id"])		
            except ValueError:
                pass
                file.write("\n")
            line = tweets_file.readline()	
        tweets_file.close()
    file.close()

    print "Number of Flagged Tweets:"	
    print count

    count = 0
    file = open("Flagged_Oxycontin_Users.txt","w")
    for users in flagged_users:
        file.write(str(users))
        file.write("\n")
        count = count + 1
    file.close()

    print "Number of Flagged Users"
    print count

if __name__ == "__main__":
    main()
