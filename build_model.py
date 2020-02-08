# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
# https://www.analyticsvidhya.com/blog/2018/07/hands-on-sentiment-analysis-dataset-python/

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, casual_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random, csv

'''
Module uses NLTK Twitter samples to build a sentiment analysis model
using a Niave Bayes Classifier. Accuracy is 99.5%.
'''

def import_csv(csv_filename):
	# append .csv filetype if not included
	if not csv_filename.endswith('.csv'):
		csv_filename = csv_filename + '.csv'

	data = []

	# save csv data
	with open(csv_filename, newline='') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			data.extend(row)

	return data


def remove_noise(tweet_tokens, stop_words = ()):
	'''
	Utility function to get cleaned alphanumeric word tokens.
	Remove URL hyperlinks, @ mentions, punctuation and specials characters.
	Removes stop words and normalizes word forms.

	Arguments:
		tweet_tokens: Tokens to be cleaned.
		stop_words: Stop words as list of strings.

	Returns:
		cleaned_tokens: Cleaned tokens.
	'''

	cleaned_tokens = []

	for token, tag in pos_tag(tweet_tokens):
		# replace URL hyperlinks with an empty string
		token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
					   '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
		# replace @ mentions with an empty string
		token = re.sub("(@[A-Za-z0-9_]+)",'', token)

		# normalize word forms using lemmatizer
		if tag.startswith("NN"):
			pos = 'n'
		elif tag.startswith('VB'):
			pos = 'v'
		else:
			pos = 'a'

		lemmatizer = WordNetLemmatizer()

		# get normalized tokens
		token = lemmatizer.lemmatize(token, pos)

		# remove punctuation, special characters and stop words
		if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
			cleaned_tokens.append(token.lower())
	return cleaned_tokens

def get_all_words(cleaned_tokens_list):
	'''
	Utility function to iterate through a list of tokens.

	Arguments:
		cleaned_tokens_list: A list of tokens.

	Yields:
		token: Each token from given list.
	'''
	for tokens in cleaned_tokens_list:
		for token in tokens:
			yield token

def get_tweets_for_model(cleaned_tokens_list):
	'''
	Utility function to format tokens as a dictionary for a model.

	Arguments:
		cleaned_tokens_list: A list of tokens.

	Yields:
		Generator function for tokens as a dictionary.
	'''
	for tweet_tokens in cleaned_tokens_list:
		yield dict([token, True] for token in tweet_tokens)

def main():
	# set nltk twitter samples as list of strings
	pos_sample_tweets = twitter_samples.strings('positive_tweets.json')
	neg_sample_tweets = twitter_samples.strings('negative_tweets.json')

	# get custom tweets as list of strings
	pos_custom_tweets = import_csv('positive_tweets.csv')
	neg_custom_tweets = import_csv('negative_tweets.csv')

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
		positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

	# get cleaned negative tokens
	for tokens in negative_tweet_tokens:
		negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

	# convert tokens into iterable word lists
	all_pos_words = get_all_words(positive_cleaned_tokens_list)
	all_neg_words = get_all_words(negative_cleaned_tokens_list)

	# get frequency distribution of word lists
	freq_dist_pos = FreqDist(all_pos_words)
	freq_dist_neg = FreqDist(all_neg_words)

	# print top 10 positive and negative words
	print(freq_dist_pos.most_common(10))
	print(freq_dist_neg.most_common(10))

	# convert tokens to a dictionary for modelling
	positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
	negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

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

	return classifier

	# # test model with custom text
	# custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
	# custom_tokens = remove_noise(word_tokenize(custom_tweet))

	# # print custom tweet and label probabilities
	# dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))
	# for label in dist.samples():
	# 	print(custom_tweet, "%s: %f" % (label, dist.prob(label)))


if __name__ == "__main__":
	main()