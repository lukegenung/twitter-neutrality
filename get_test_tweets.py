import clean_text
import tweepy
from tweepy import OAuthHandler

'''
TESTING module. Can be used to retrieve 1 tweet at a time.
Calls clean_text.py to test text parsing capability.
'''

# number of tweets
count = 1

# keys and tokens from the Twitter Dev Console
consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'

# attempt authentication
try:
	# create OAuthHandler object
	auth = OAuthHandler(consumer_key, consumer_secret)
	# set access token and secret
	auth.set_access_token(access_token, access_token_secret)
	# create tweepy API object to fetch tweets
	api = tweepy.API(auth)
except:
	print("Error: Authentication Failed")

# get tweets
tweets = []
try:
	# call twitter api to fetch tweets
	fetched_tweets = api.search(q = 'Donald Trump', count = 1, tweet_mode = 'extended')
	# parsing tweets one by one
	for tweet in fetched_tweets:
		# empty dictionary to store required params of a tweet
		parsed_tweet = {}
		# saving tweet text (or retweet text if RT)
		if hasattr(tweet, 'retweeted_status'):
			parsed_tweet['text'] = tweet.retweeted_status.full_text
		else:
			parsed_tweet['text'] = tweet.full_text
		# appending parsed tweet to tweets list
		if tweet.retweet_count > 0:
			# if tweet has retweets, ensure that it is appended only once
			if parsed_tweet not in tweets:
				tweets.append(parsed_tweet)
		else:
			tweets.append(parsed_tweet)
except tweepy.TweepError as e:
	# print error (if any)
	print("Error : " + str(e))

# test clean_text.py on each tweet
for tweet in tweets:
	a = clean_text.main(tweet['text'], normalize = True)