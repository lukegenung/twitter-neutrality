import api_keys
import tweepy
from tweepy import OAuthHandler

def main():
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

if __name__ == '__main__':
	main()