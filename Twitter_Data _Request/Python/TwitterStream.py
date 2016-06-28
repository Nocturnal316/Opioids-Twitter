from twython import TwythonStreamer
import json
import pickle

jsonFile = open("ourtweets.json","w")
consumer_key = ""
consumer_secret = "
access_token = ""
access_token_secret = ""

class MyStreamer(TwythonStreamer):
    
    def on_success(self, data):
        global jsonFile
        if 'text' in data:
            #jdata = json.dumps(data)
            #jobject = json.loads(jdata)
            #print(jobject["lang"].values())
            print data['text'].encode('utf-8')
            print("/n")
            
            jsonFile.write("{")
            jsonFile.write('"lang": '+str('"'+data["lang"]+'",'))
            jsonFile.write('"source": '+str('"'+data["source"]+'",'))
            jsonFile.write('"text": '+str('"'+data["text"].encode('utf-8')+'",'))
            jsonFile.write('"created_at": '+str('"'+data["created_at"]+'",'))
            jsonFile.write('"filter_level": '+str('"'+data["filter_level"]+'",'))
            #jsonFile.write('"place": {')
            #jsonFile.write("}")
            #jsonFile.write(str(data["user"]))
            jsonFile.write("}")
##            jsonFile.write(str(sdata["id"]))
##            jsonFile.write(";")
##            jsonFile.write(str(sdata["user"]["id_str"]))
##            jsonFile.write(";")
##            #jsonfile.write(str(temp))
##            #jsonfile.write(";")
##            jsonFile.write(str(sdata["created_at"])[5:25])
##            jsonFile.write(";")
##            jsonFile.write(str(jdata["text"].encode('unicode-escape')))
##            jsonFile.write("\n")
##            #jsonFile.write(json.dumps(data)+"\n")

    def on_error(self, status_code, data):
        print status_code
        #sleep(3000)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


topics = ""


stream = MyStreamer(consumer_key, consumer_secret,
                    access_token, access_token_secret)
stream.statuses.filter(track='america')
		
		


##https://dev.twitter.com/overview/api/tweets
##{
##  "lang": "en",
##  "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
##  "text": "Let's be alone together, we can stay young forever.",
##  "created_at": "Mon, 09 Dec 2013 00:00:02 +0000",
##  "filter_level": "medium",
##  "place": {
##    "name": "Batavia",
##    "url": "https://api.twitter.com/1.1/geo/id/4c794ce21ef49219.json",
##    "country": "United States",
##    "place_type": "city",
##    "full_name": "Batavia, NY",
##    "country_code": "US",
##    "id": "4c794ce21ef49219"
##  },
##  "user": {
##    "lang": "en",
##    "favourites_count": 6598,
##    "description": "Contrary to popular belief, i'm not actually a senior.",
##    "friends_count": 298,
##    "created_at": "Mon, 28 May 2012 20:07:53 +0000",
##    "verified": false,
##    "location": "Class of 2014",
##    "profile_image_url": "http://pbs.twimg.com/profile_images/378800000827310277/9fd13ea896f0fb134a442b5f06c0212d_normal.jpeg",
##    "name": "HaleyCase",
##    "profile_image_url_https": "https://pbs.twimg.com/profile_images/378800000827310277/9fd13ea896f0fb134a442b5f06c0212d_normal.jpeg",
##    "followers_count": 473,
##    "screen_name": "Haley_Wynne",
##    "id_str": "593023079",
##    "statuses_count": 11537,
##    "geo_enabled": true,
##    "id": 593023079,
##    "listed_count": 0
##  },
##  "geo": {
##    "latitude": 43.0090509,
##    "longitude": -78.1759921
##  },
##  "id": "409834786367098880"
##}
