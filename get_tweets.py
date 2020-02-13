import twitter_client
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
import re, csv, time

'''
Send search queries to Twitter API to get tweet data.
API calls are kept within Twitter's rate limits (18K tweets every 15 minutes).
Return tweet data.
'''

def get_tweets(api, query, results_needed, tweets):
	'''
	Get tweet data from Twitter Search endpoint.

	Arguments:
		api: Twitter API client object.
		query: Twitter search query as string. Include multiple values using '+AND+' or '+OR+'.
		results_needed: Number of tweets requested as integer.
		tweets: Tweets already collected as a list of dictionaries.
	Returns:
		fetched_tweets_list: Tweets as a list of dictionaries.
	'''
	
	fetched_tweets_list = []

	try:
		# call twitter api to fetch a sample of tweets
		fetched_tweets = api.search(q = query, lang = 'en', result_type = 'popular', count = results_needed, tweet_mode = 'extended')

		for tweet in fetched_tweets:
			# empty dictionary to store required params of a tweet
			parsed_tweet = {}

			# save basic info
			parsed_tweet['id'] = tweet.id
			parsed_tweet['screen_name'] = tweet.user.screen_name
			parsed_tweet['status'] = tweet.full_text

			# skip retweets and duplicate tweets
			if hasattr(tweet, 'retweeted_status') or parsed_tweet['id'] in tweets:
				continue
			
			# save new tweet data
			fetched_tweets_list.append(parsed_tweet)

	except tweepy.TweepError as e:
		# print error (if any)
		print("Error : " + str(e))

	return fetched_tweets_list


def main(query, results = 10):
	'''
	Main calling function to get Twitter data and rate limit API calls.

	Arguments:
		query: Twitter search query as string. Include multiple values using '+AND+' or '+OR+'.
		results: Number of tweets requested as integer.
	Returns:
		tweets: Tweets as a list of dictionaries.
	'''
	if query == None:
		print('Must provide a Twitter search query!')
		return

	# Start API client
	api = twitter_client.main()
	
	tweets = []			# empty list to store tweets
	call_count = 0
	rate_limit = 180	# 180 API calls allowed per 15 mins (900 secs)
	sleep_time = 900	# 15 min sleep time (900 secs)

	results_needed = results

	while results_needed > 0:
		tweets.extend(get_tweets(api, query, results_needed, tweets))

		# number of results still needed
		tweet_count = len([d for d in tweets])
		results_needed = results - tweet_count
		print('Tweets still needed: ', results_needed)

		# rate limit API calls 
		# maximum tweets per API call is 100
		# maximum API calls is 180 per 15 mins (or 18,000 tweets per 15 mins)
		call_count += 1
		if call_count >= rate_limit:
			time.sleep(sleep_time)
			call_count = 0

		print('Search API calls submitted: ', call_count)
		print('# of tweets retrieved: ', tweet_count)
	
	print('Collected requested tweet count!')

	return tweets


if __name__ == '__main__':
	main(query = 'Donald Trump')