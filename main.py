import build_model, get_tweets, get_sentiment, post_reply
from nltk.tokenize import casual_tokenize
from nltk import classify

# classifier = build_model.main()

''' 
## Classifier usage example:
custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
custom_tokens = build_model.remove_noise(casual_tokenize(custom_tweet))

## Get positive/negative probability for custom tweet
dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))

for label in dist.samples():
	print(custom_tweet, "%s: %f" % (label, dist.prob(label)))
'''

# Get tweets from Twitter API as a list of dicts
tweets = get_tweets.main(query = 'Donald Trump+AND+?', results = 2)

# Get sentiment of tweets
# data = get_sentiment.main(classifier, tweets)

# Reply to tweets
reply = post_reply.main(tweets)