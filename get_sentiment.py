from nltk.tokenize import casual_tokenize
import build_model

'''
Module does stuff.
'''

def get_distribution(classifier, tweets):
	'''
	Takes tweets as a list of dictionaries.
	Get distribution of positive and negative sentiment probability for each tweet.
	Returns tweets as a list of dictionaries with sentiment labels.

	Arguments:
		classifier: NLTK Naive Bayes Classifier object.
		tweets: Tweets as a list of dictionaries.
	Returns:
		tweets: Tweets as a list of dictionaries.
	'''
	# set empty lists to store distribution
	pos_probability = []
	neg_probability = []

	# get positive and negative probabilities for each tweet
	for tweet in tweets:
		custom_tokens = build_model.remove_noise(casual_tokenize(tweet['status']))
		dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))

		# append probabilites to list
		pos_probability.append(dist.prob('Positive'))
		neg_probability.append(dist.prob('Negative'))

	# add sentiment probabilities to tweet dictionary
	try:
		tweet['positive'] = pos_probability
		tweet['negative'] = neg_probability
	except Exception as e:
		print(e)

	# add sentiment label to tweet dictionary
	if pos_probability > neg_probability:
		tweet['label'] = 'Positive'
	elif neg_probability > pos_probability:
		tweet['label'] = 'Negative'
	else:
		tweet['label'] = 'None'

	print('Sentiment distribution calculations completed.')

	return tweets


def main(classifier, tweets):
	data = get_distribution(classifier, tweets)