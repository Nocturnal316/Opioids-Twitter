#! /bin/bash

clear

echo $'Running drug_tweet_searcher.py\n'
python drug_tweet_searcher.py
echo $'\n\n'

echo $'Running oxycontin_connections.py\n'
python oxycontin_connections.py

echo $'\n\n'
echo $'Running oxycontin_tweet_searcher\n'

python oxycontin_tweet_searcher.py $1


echo $'\n\n'
echo $'Running oxycontin_tweet_searcher_json\n'

python oxycontin_tweet_searcher_json.py $1


echo  $'\n\n'

echo  $'Running oxycontin_users_tweets\n'
python oxycontin_users_tweets.py $1

echo $'\n\n'
echo $'All Scripts finish running\n'
