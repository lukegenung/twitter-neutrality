'''
Module uses NLTK Twitter samples to build a sentiment analysis model
using a Naive Bayes Classifier. Accuracy is 99.5%.

Based on: https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
And: https://www.analyticsvidhya.com/blog/2018/07/hands-on-sentiment-analysis-dataset-python/
'''

import helpers
from nltk.corpus import twitter_samples, stopwords
from nltk.tokenize import word_tokenize, casual_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import random


def main():
	print('Building model...')
	print('Gathering training data...')

	# set nltk twitter samples as list of strings
	pos_sample_tweets = twitter_samples.strings('positive_tweets.json')
	neg_sample_tweets = twitter_samples.strings('negative_tweets.json')

	#### UPDATE HERE: Option to add your own tweet samples
	#### Remove the empty list, uncomment and update filepaths below
	pos_custom_tweets = [] ## helpers.import_csv('positive_tweets.csv')
	neg_custom_tweets = [] ## helpers.import_csv('negative_tweets.csv')

	# combine nltk twitter samples and custom tweets
	positive_tweets = pos_sample_tweets + pos_custom_tweets
	negative_tweets = neg_sample_tweets + neg_custom_tweets

	# tokenize tweets
	positive_tweet_tokens = [casual_tokenize(i) for i in positive_tweets]
	negative_tweet_tokens = [casual_tokenize(i) for i in negative_tweets]

	# set cleaned tokens lists
	positive_cleaned_tokens_list = []
	negative_cleaned_tokens_list = []

	stop_words = stopwords.words('english')

	# get cleaned positive tokens
	for tokens in positive_tweet_tokens:
		positive_cleaned_tokens_list.append(helpers.remove_noise(tokens, stop_words))

	# get cleaned negative tokens
	for tokens in negative_tweet_tokens:
		negative_cleaned_tokens_list.append(helpers.remove_noise(tokens, stop_words))

	# convert tokens into iterable word lists
	all_pos_words = helpers.get_all_words(positive_cleaned_tokens_list)
	all_neg_words = helpers.get_all_words(negative_cleaned_tokens_list)

	# get frequency distribution of word lists
	freq_dist_pos = FreqDist(all_pos_words)
	freq_dist_neg = FreqDist(all_neg_words)

	# print top 10 positive and negative words
	print('Top 10 positive and negative words:')
	print(freq_dist_pos.most_common(10))
	print(freq_dist_neg.most_common(10))

	# convert tokens to a dictionary for modelling
	positive_tokens_for_model = helpers.get_tweets_for_model(positive_cleaned_tokens_list)
	negative_tokens_for_model = helpers.get_tweets_for_model(negative_cleaned_tokens_list)

	# assign a label to positive tokens
	positive_dataset = [(tweet_dict, "Positive")
						 for tweet_dict in positive_tokens_for_model]

	# assign a label to negative tokens
	negative_dataset = [(tweet_dict, "Negative")
						 for tweet_dict in negative_tokens_for_model]

	# set dataset and randomize to train model
	dataset = positive_dataset + negative_dataset
	random.shuffle(dataset)

	# split the data into a 70:30 ratio among 10K tweets
	train_data = dataset[:7000]
	test_data = dataset[7000:]

	# train a Naive Bayes model
	classifier = NaiveBayesClassifier.train(train_data)

	# print model accuracy
	print("Model accuracy is:", classify.accuracy(classifier, test_data))
	print(classifier.show_most_informative_features(10))
	print('Model complete!\n')

	return classifier