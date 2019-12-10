import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'XXX'
		consumer_secret = 'XXX'
		access_token = 'XXX'
		access_token_secret = 'XXX'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to get sentiment polarity and subjectivity
		of passed tweet using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# get polarity and subjectivity as list
		return analysis.sentiment

	def get_tweet_polarity(self, tweet): 
		''' 
		Utility function to classify sentiment polarity of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = []

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving user data
				parsed_tweet['screen_name'] = tweet.user.screen_name
				parsed_tweet['followers_count'] = tweet.user.followers_count
				parsed_tweet['verified'] = tweet.user.verified

				# saving tweet data
				parsed_tweet['url'] = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str
				parsed_tweet['text'] = tweet.text
				parsed_tweet['polarity'] = "{:.1%}".format(self.get_tweet_sentiment(tweet.text)[0])
				parsed_tweet['subjectivity'] = "{:.1%}".format(self.get_tweet_sentiment(tweet.text)[1])
				parsed_tweet['sentiment'] = self.get_tweet_polarity(tweet.text)
				parsed_tweet['time'] = tweet.created_at
				parsed_tweet['retweet_count'] = tweet.retweet_count
				parsed_tweet['favorite_count'] = tweet.favorite_count

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e))

def print_results(tweet):
	# score tweet engagement
	if tweet['verified']:
		visibility = 1.5 * tweet['followers_count']
	else:
		visibility = tweet['followers_count']
	activity = tweet['favorite_count'] + tweet['retweet_count']	# add reply count
	engagement = round(activity / visibility, 2)

	print('URL: ' + tweet['url'])
	print('User: ' + tweet['screen_name'] + ' (' + str(tweet['time']) + ')')
	print('Text: ' + tweet['text'])
	print('Followers: ' + str(tweet['followers_count']))
	print('Verified: ' + str(tweet['verified']))
	print('Engagement: ' + str(engagement))
	print('Polarity: ' + tweet['polarity'])
	print('Subjectivity: ' + tweet['subjectivity'])


def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = 'Donald Trump', count = 200) 

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	# picking negative tweets from tweets 
	ngtweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(100*len(ngtweets)/len(tweets))) 
	# picking negative tweets from tweets 
	nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
	# percentage of negative tweets 
	print("Neutral tweets percentage: {} %".format(100*len(nutweets)/len(tweets))) 

	# printing first positive tweet
	print("\n\nPositive tweets:") 
	for tweet in ptweets[:1]:
		print_results(tweet)

	# printing first negative tweet
	print("\n\nNegative tweets:") 
	for tweet in ngtweets[:1]: 
		print_results(tweet)

	# printing first neutral tweet
	print("\n\nNeutral tweets:") 
	for tweet in nutweets[:1]: 
		print_results(tweet)

if __name__ == "__main__": 
	# calling main function 
	main() 
