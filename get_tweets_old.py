import clean_text, sent_analysis
import re, tweepy
from tweepy import OAuthHandler

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

	def get_tweets(self, query, count = 20):
		'''
		Main function to fetch tweets and parse the data.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count, tweet_mode = 'extended')

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving user data
				parsed_tweet['screen_name'] = tweet.user.screen_name
				parsed_tweet['followers_count'] = tweet.user.followers_count
				parsed_tweet['verified'] = tweet.user.verified

				# saving tweet text (or retweet text if RT)
				if hasattr(tweet, 'retweeted_status'):
					parsed_tweet['text'] = tweet.retweeted_status.full_text
					parsed_tweet['is_retweet'] = 'True'
				else:
					parsed_tweet['text'] = tweet.full_text
					parsed_tweet['is_retweet'] = 'False'

				parsed_tweet['clean_text'] = clean_text.main(parsed_tweet['text'], spell_check = False)

				# saving tweet data
				parsed_tweet['url'] = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str
				parsed_tweet['time'] = tweet.created_at
				parsed_tweet['retweet_count'] = tweet.retweet_count
				parsed_tweet['favorite_count'] = tweet.favorite_count

				# get tweet sentiment data
				parsed_tweet['polarity'] = "{:.1%}".format(sent_analysis.get_sentiment(parsed_tweet['clean_text'])[0])
				parsed_tweet['subjectivity'] = "{:.1%}".format(sent_analysis.get_sentiment(parsed_tweet['clean_text'])[1])
				parsed_tweet['sentiment'] = sent_analysis.get_pattern_cat(parsed_tweet['clean_text'])
				parsed_tweet['nb_sentiment'] = sent_analysis.get_nb_cat(parsed_tweet['clean_text'])

				# score tweet engagement
				if parsed_tweet['verified']:
					parsed_tweet['visibility'] = 1.5 * parsed_tweet['followers_count']
				else:
					parsed_tweet['visibility'] = parsed_tweet['followers_count']

				# add reply count
				parsed_tweet['activity'] = parsed_tweet['favorite_count'] + parsed_tweet['retweet_count']
				 # if no followers, engagement = 0
				parsed_tweet['engagement'] = round(parsed_tweet['visibility'] / parsed_tweet['visibility'], 2) if parsed_tweet['visibility'] else 0

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

	def pick_tweets(self, tweets):
		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		# percentage of positive tweets
		print("\nPOSITIVE TWEETS percentage: {} %".format(100*len(ptweets)/len(tweets)))
		# picking negative tweets from tweets
		ngtweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		# percentage of negative tweets
		print("NEGATIVE TWEETS percentage: {} %".format(100*len(ngtweets)/len(tweets)))
		# picking negative tweets from tweets
		nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
		# percentage of negative tweets
		print("NEUTRAL TWEETS percentage: {} %".format(100*len(nutweets)/len(tweets)))

		return ptweets, ngtweets, nutweets

	def print_results(self, tweet):
		print('URL: ', tweet['url'])
		print('User: ', tweet['screen_name'], ' (', str(tweet['time']), ')')
		print('Full Text: \n', tweet['text'])
		print('Clean text (sentiment analysis): \n', tweet['clean_text'])
		print('Followers: ', tweet['followers_count'])
		print('Verified: ', tweet['verified'])
		print('Engagement: ', tweet['engagement'])
		print('Pattern Category: ', tweet['sentiment'])
		print('Pattern Polarity: ', tweet['polarity'])
		print('Pattern Subjectivity: ', tweet['subjectivity'])
		print('Naive Bayes Category: ', tweet['nb_sentiment'][0])
		print('Naive Bayes p_pos: ', "{:.1%}".format(tweet['nb_sentiment'][1]))
		print('Naive Bayes p_neg: ', "{:.1%}".format(tweet['nb_sentiment'][2]))
		print('\n')


def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	query = api.get_tweets(query = 'Donald Trump', count = 20)

	# categorize tweets based on sentiment
	ptweets, ngtweets, nutweets = api.pick_tweets(query)
	# printing first positive tweet
	print("\nPositive tweets:")
	for tweet in ptweets[:3]:
		api.print_results(tweet)
	# printing first negative tweet
	print("\nNegative tweets:")
	for tweet in ngtweets[:3]:
		api.print_results(tweet)
	# printing first neutral tweet
	print("\nNeutral tweets:")
	for tweet in nutweets[:3]:
		api.print_results(tweet)

if __name__ == "__main__":
	# calling main function
	main()
