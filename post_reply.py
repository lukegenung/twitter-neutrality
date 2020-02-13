import twitter_client
import random
import tweepy
from tweepy import OAuthHandler

'''
Loop through each fetched tweet and post a randomly selected reply.
Rate limited to 300 API calls per 3 hours to the POST status endpoint.
'''

def set_reply_text():
	'''
	Set text to use for reply. Randomize which text to use.
	'''
	reply_a = 'I have no strong feelings one way or the other.'
	reply_b = 'All I know is my gut says maybe.'

	# randomize reply text
	x = random.randint(0, 1)

	if x == 0:
		text = reply_a
	else:
		text = reply_b

	return text


def main(tweets):
	# Start API client
	api = twitter_client.main()

	# Rate limit API calls
	call_count = 0
	rate_limit = 180	# 300 API calls allowed per 3 hours (10800 secs)
	sleep_time = 10800	# 3 hour sleep time (10800 secs)

	for tweet in tweets:
		# Setup reply for fetched tweets
		reply_to = tweet['screen_name']
		text = set_reply_text()
		reply = '@' + reply_to + ' ' + text
		status_id = tweet['id']

		try:
			# Post reply to fetched tweets
			api.update_status(status = reply, in_reply_to_status_id = status_id, auto_populate_reply_metadata = True)
		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

		# Sleep after reaching rate limit
		call_count += 1
		if call_count >= rate_limit:
			time.sleep(sleep_time)
			call_count = 0

		print('POST status API endpoint calls submitted: ', call_count)