'''
Helper functions to clean text data for analysis, read and write csv files.
'''

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from collections import Counter
import csv, time, re, string


def import_csv(csv_filename):
	data = []

	# add '.csv' type if not included in csv_filename
	if not csv_filename.endswith('.csv'):
		csv_filename = csv_filename + '.csv'

	# save csv data
	with open(csv_filename, newline='') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			data.extend(row)

	return data


def write_to_scv(tweets):
	'''
	Write tweets to a new csv.
	'''

	# name csv file
	timestr = time.strftime("%Y%m%d-%H%M%S")
	new_filename = 'tweets-' + timestr + '.csv'

	# write to csv file
	header = tweets[0].keys()
	with open(new_filename, 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, header)
		dict_writer.writeheader()
		dict_writer.writerows(tweets)


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