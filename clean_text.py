# Data Pre-processing and Feature Engineering
from textblob import TextBlob
import re, inspect
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class CleanText(object):
	'''
	Text Class for removing punctuation, stop words and lexicon normalization. 
	'''
	def clean_tweet(self, tweet):
		'''
		Utility function to remove URLs, usernames and normalize capitalization.
		Takes a string and returns a string.
		'''
		# remove URLs
		tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)
		# remove usernames
		tweet = re.sub('@[^\s]+', '', tweet)
		# show output
		# print(inspect.currentframe().f_code.co_name, ': \n', tweet, '\n')
		return tweet

	def spell_correct(self, text):
		'''
		Utility function to correct spelling errors.
		Takes a string and returns a string.
		'''
		text_blob = TextBlob(text)
		corr_str = str(text_blob.correct())
		# show output
		# print(inspect.currentframe().f_code.co_name, ': \n', corr_str, '\n')
		return corr_str

	def clean_punc(self, text):
		'''
		Utility function to clean text by removing punctuation.
		Takes a string and return a string.
		'''
		# remove &amp;
		new_text = re.sub('&amp;', '', text)
		# get word list
		text_blob = TextBlob(new_text)
		# convert word list to a string
		word_list = ' '.join(text_blob.words)
		# show output
		# print(inspect.currentframe().f_code.co_name, ': \n', word_list, '\n')
		return word_list

	def word_list(self, text):
		'''
		Utility function to clean text by removing stop words, symbols and numbers.
		Takes a string as input and returns a list.
		'''
		# convert string to a list of words
		element_list = [ele for ele in text.split()]
		# remove symbols and numbers
		clean_tokens = [t for t in element_list if re.match(r'[^\W\d]*$', t)]
		# convert list to a string
		clean_s = ' '.join(clean_tokens)
		# remove stop words
		word_list = [word for word in clean_s.split() if word.lower() not in stopwords.words('english')]
		# show output
		# print(inspect.currentframe().f_code.co_name, ': \n', word_list, '\n')
		return word_list

	def normalization(self, word_list):
		'''
		Utility function to normalize words with the same meaning, i.e. 'went' -> 'go'
		Takes a list as input and return a list.
		'''
		lem = WordNetLemmatizer()
		new_list = []
		for word in word_list:
			normalized_word = lem.lemmatize(word,'v')
			new_list.append(normalized_word)
		# show output
		# print(inspect.currentframe().f_code.co_name, ': \n', new_list, '\n')
		return new_list

	def get_clean_text(self, text, is_tweet, spell_check, normalize):
		'''
		Main function to build a clean word list from given text.
		'''
		# print starting text
		print('Starting text: ', '\n', text, '\n')
		# convert text to lower-case
		text = text.lower()
		# if text is a tweet, run additional cleaning
		if is_tweet:
			text = self.clean_tweet(text)
		# correct spelling errors
		if spell_check:
			text = self.spell_correct(text)
		# remove punctuation
		text = self.clean_punc(text)
		# get a word list with no stop words, symbols or numbers
		word_list = self.word_list(text)
		# normalize words with the same meaning
		if normalize:
			word_list = self.normalization(word_list)
		# convert word list to a string
		clean_text = ' '.join(word_list)
		# print ending text
		print('Ending text: ', '\n', clean_text, '\n')
		return clean_text


def main(text, is_tweet = True, spell_check = True, normalize = True):
	# creating object of CleanText class
	t = CleanText()
	# calling main function
	clean_text = t.get_clean_text(text, is_tweet, spell_check, normalize)
	return clean_text