from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def get_sentiment(text):
	'''
	Utility function to get sentiment polarity and subjectivity
	of passed tweet using textblob's sentiment method
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(text)
	# get polarity and subjectivity as list
	return analysis.sentiment

def get_pattern_cat(text):
	'''
	Utility function to classify Pattern polarity of passed tweet
	using textblob's default sentiment method.
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(text)
	# set Pattern classification
	if analysis.sentiment.polarity > 0:
		return 'positive'
	elif analysis.sentiment.polarity == 0:
		return 'neutral'
	else:
		return 'negative'

def get_nb_cat(text):
	'''
	Utility function to classify Naive Bayes category of passed tweet
	using textblob's Naive Bayes sentiment method.
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(text, analyzer = NaiveBayesAnalyzer())
	# set Naive Bayes classification
	nb = analysis.sentiment
	return nb