import api_keys
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
import re, csv, time

'''
Module sends queries to Twitter API Search endpoint.
Saves the original query and tweet results to a CSV.
API calls are kept within Twitter's rate limits (18,0000 tweets every 15 minutes).
'''

def twitter_client():
	'''
	Utility function to authenticate the session with Twitter API.
	'''
	# keys and tokens from the Twitter Dev Console
	consumer_key = api_keys.consumer_key()
	consumer_secret = api_keys.consumer_secret()
	access_token = api_keys.access_token()
	access_token_secret = api_keys.access_token_secret()

	# attempt authentication
	try:
		# create OAuthHandler object
		auth = OAuthHandler(consumer_key, consumer_secret)
		# set access token and secret
		auth.set_access_token(access_token, access_token_secret)
		# create tweepy API object to fetch tweets
		api = tweepy.API(auth)
		return api
	except:
		print("Error: Authentication Failed")

def get_tweets(api, query, results):
	'''
	Main function to get tweet data from Twitter Search endpoint.
	Maximum tweets per API call is 100.
	Maximum API calls is 180 per 15 mins (or 18,000 tweets per 15 mins).
	'''
	tweets = []			# empty list to store tweets
	tweet_num = 0		# counter for tweets returned from API
	call_count = 0
	rate_limit = 180	# 180 API calls allowed per 15 mins (900 secs)
	sleep_time = 900	# 15 min sleep time (900 secs)
	

	results_needed = results

	while results_needed > 0:
		try:
			# call twitter api to fetch a sample of tweets
			fetched_tweets = api.search(q = query, count = results_needed, tweet_mode = 'extended')

			for tweet in fetched_tweets:
				# saving tweet text (or retweet text if it is RT)
				if hasattr(tweet, 'retweeted_status'):
					text = tweet.retweeted_status.full_text
				else:
					text = tweet.full_text

				# print tweets returned by API
				tweet_num +=1
				print(tweet_num, '\n', text, '\n')

				# do not store duplicate tweets
				if text not in tweets:
					tweets.append(text)
				else:
					pass

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

		# number of results still needed
		results_needed = results - len(tweets)

		# if rate limit is reached then sleep
		call_count += 1
		if call_count >= rate_limit:
			time.sleep(sleep_time)
			call_count = 0

	print('All queries complete: ', call_count)
	print('# of tweets retrieved: ', len(tweets))

	return tweets


def save_tweets_to_csv(query, tweets):
	'''
	Utility function to save Twitter data to csv.
	'''
	# get name for new data file using current datetime
	now = datetime.now()
	tweet_filename = re.sub(r'[^\w]','_',now.strftime("%Y/%m/%d %H:%M:%S")) + '.csv'

	# write tweets to the new data file
	with open(tweet_filename,'w') as csvfile:
		linewriter = csv.writer(csvfile,delimiter=',',quotechar="\"")
		linewriter.writerow(['query', 'tweet'])
		for tweet in tweets:
			try:
				linewriter.writerow([query, tweet])
			except Exception as e:
				print(e)


def main(query = 'Donald Trump', results = 10):
	api = twitter_client()
	tweets = get_tweets(api, query, results)
	save_data = save_tweets_to_csv(query, tweets)


if __name__ == '__main__':
	main(results=2000)
