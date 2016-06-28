from twython import TwythonStreamer
import json

jsonFile = open("allTweets.json","w")
consumer_key = "IYI98EkHxXsNXivYX7xm19eOi"
consumer_secret = "ByPKtxN0rFKhCGeWhloGHsV5tMnB1mYxgZTiAKDDyAt3aFKC3S"
access_token = "788587562-H44SFWDYPH2tAEjKPSLOopjddWHeFlq6Izi2d9Jj"
access_token_secret = "5Wd7iIJrB2PMS5m4kT9cApljKUtLjUItVHdpZHkQh3i6E"


class MyStreamer(TwythonStreamer):
    
    def on_success(self, data):
        global jsonFile
        if 'text' in data:
            jsonFile.write(json.dumps(data)+"\n")

    def on_error(self, status_code, data):
        print status_code
        sleep(300)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()







stream = MyStreamer(consumer_key, consumer_secret,access_token, access_token_secret)
stream.statuses.filter(track='twitter')
		
		

