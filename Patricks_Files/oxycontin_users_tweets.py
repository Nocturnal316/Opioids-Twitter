import json
import codecs
import sys

def main ():
    #tweets_file = open("1year_filtered.json")
    #flagged_users_file = open("Flagged_Oxycontin_Users.txt")
    #flagged_users_file = open("Oxycontin_Yes_Histogram.txt")
    flagged_users_file = open(".\TextFiles\Hand_Flagged_Users.txt",'r')

    triangle_users_file = open(".\TextFiles\Oxycontin_User_Triangle_Thirds.txt",'r')

    #oxy_tweets = set()
    flagged_users = set()
    triangle_users = set()
   
   
    iterargs = iter(sys.argv)
  
    next(iterargs)
    for x in iterargs:
        
        tweets_file = open(x)
    
        line = flagged_users_file.readline()
        while line != "":
            try:
                flagged_users.add(int(line))
                line = flagged_users_file.readline()
            except ValueError:
                pass
                line = flagged_users_file.readline()
        flagged_users_file.close()

        line = triangle_users_file.readline()
        while line != "":
            try:
                triangle_users.add(int(line))
                line = triangle_users_file.readline()
            except ValueError:
                pass
                line = triangle_users_file.readline()
        triangle_users_file.close()

        #print flagged_users

        found_users = set()
        found_tris = set()

        file = open(".\TextFiles\Flagged_Users_Tweets.txt","w")
        tris = open(".\TextFiles\Triangle_Users_Tweets.txt",'w')
        line = tweets_file.readline()
        
        while line != "":
            try:
                j = json.loads(line.lower())
                #if j["id"] not in oxy_tweets:
                    #print j["user"]
                if int(j["user"]["id_str"]) in flagged_users:
                    file.write(str(j["id"]))
                    file.write(";")
                    file.write(str(j["user"]["id_str"]))
                    file.write(";")
                    file.write(str(j["created_at"])[5:25])
                    file.write(";")
                    file.write(str(j["text"].encode('unicode-escape')))
                    file.write("\n")
                    #oxy_tweets.add(j["id"])
                    if int(j["user"]["id_str"]) not in found_users:
                        found_users.add(int(j["user"]["id_str"]))
                if int(j["user"]["id_str"]) in triangle_users:
                    tris.write(str(j["id"]))
                    tris.write(";")
                    tris.write(str(j["user"]["id_str"]))
                    tris.write(";")
                    tris.write(str(j["created_at"])[5:25])
                    tris.write(";")
                    tris.write(str(j["text"].encode('unicode-escape')))
                    tris.write("\n")
                    if int(j["user"]["id_str"]) not in found_tris:
                        found_tris.add(int(j["user"]["id_str"]))		
            except ValueError:
                pass
                file.write("\n")
                tris.write("\n")
                tweets_file.close()
 
            line = tweets_file.readline()	
        tweets_file.close()
        file.close()
        tris.close()

        
        print "Number of Oxy User's Twitterings Sought:"
        print len(flagged_users)
        print "Number of Oxy User's Twitterings Found:"
        print len(found_users)
        print "Number of Triangle User's Twitterings Sought:"
        print len(triangle_users)
        print "Number of Triangle User's Twitterings Found:"
        print len(found_tris)

if __name__ == "__main__":
    main()
