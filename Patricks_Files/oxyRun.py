from drug_tweet_searcher import *
from oxycontin_connections  import *
from oxycontin_tweet_searcher import *
from oxycontin_tweet_searcher_json import *
from oxycontin_users_tweets import *
import sys


######################################################
# Currently only running these two together
# as they are the only ones that make sense to running
# the others require if any a list a files to open which is better of
# to run manually from command line arguments.
######################################################
def main():
    print 'Running Search Drug Tweets'
    tweetSearch().searchDrugTweets()
    print 'Running Oxy Connections'
    oxyConnections().oxyConnectionsRun()
	
	#iterargs = iter(sys.argv)
    #next(iterargs)
    


main()
