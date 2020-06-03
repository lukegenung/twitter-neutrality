'''
Get distribution of positive and negative sentiment probability for supplied text.
'''

from nltk.tokenize import casual_tokenize
import build_model, helpers


def get_sentiment(classifier, tweets, keep_status=True):
	'''
	Takes tweets as a list of dictionaries.
	Returns tweets as a list of dictionaries with sentiment labels.

	Arguments:
		classifier: NLTK Naive Bayes Classifier object.
		tweets: Tweets as a list of dictionaries.
	Returns:
		tweets: Tweets as a list of dictionaries.
	'''

	print('Starting text analysis...')
	print('Scoring tweets...')
	# get positive and negative probabilities for each tweet
	for tweet in tweets:
		custom_tokens = helpers.remove_noise(casual_tokenize(tweet['status']))
		dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))

		# append probabilites to list
		pos_probability = dist.prob('Positive')
		neg_probability = dist.prob('Negative')

		# add sentiment probabilities to tweet dictionary
		try:
			tweet['positive'] = pos_probability
			tweet['negative'] = neg_probability
		except Exception as e:
			print(e)

		# add sentiment label to tweet dictionary
		if pos_probability >= 0.9:
			tweet['label'] = 'Very Positive'
		elif pos_probability >= 0.7:
			tweet['label'] = 'Positive'
		elif pos_probability > 0.3 and neg_probability > 0.3:
			tweet['label'] = 'Neutral'
		elif neg_probability >= 0.9:
			tweet['label'] = 'Very Negative'
		elif neg_probability >= 0.7:
			tweet['label'] = 'Negative'
		else:
			tweet['label'] = 'None'

		# optional: remove tweet status to reduce data size
		if tweet['status'] and keep_status == False:
			del tweet['status']

	print('Text analysis complete!\n')

	return tweets