from nltk.tokenize import word_tokenize
import os, contextlib
import pandas as pd
import build_model

@contextlib.contextmanager
def atomic_overwrite(filename):
	'''
	Utility function using context manager to handle atomic overwriting of CSV with new data.
	Prevents data loss if program is interrupted at the saving call.
	'''
	temp = filename + '~'
	with open(temp, "w") as f:
		yield f
	os.rename(temp, filename) # this will only happen if no exception was raised

def make_dataframe(filename):
	# load csv into a DataFrame
	data = pd.read_csv(filename)
	df = pd.DataFrame(data)
	return df

def get_distribution(data_frame, classifier):
	'''
	Add positive and negative probabilities for each tweet in Data Frame.
	'''
	# set empty lists to store distribution
	pos_probability = []
	neg_probability = []

	# get positive and negative probabilities for each tweet
	for t in data_frame['tweet']:
		print('\n', t)
		custom_tokens = build_model.remove_noise(word_tokenize(t))
		dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))
		# print label distribution
		for label in dist.samples():
			print("%s: %f" % (label, dist.prob(label)))

		# append probabilites to list
		pos_probability.append(dist.prob('Positive'))
		neg_probability.append(dist.prob('Negative'))

	# add probabilities as columns to DataFrame
	try:
		data_frame['positive'] = pos_probability
		data_frame['negative'] = neg_probability
	except Exception as e:
		print(e)

	print('Distribution calculations completed')

	return data_frame


def main(classifier, filename):
	df = make_dataframe(filename)
	df = get_distribution(df, classifier)

	# add probabilities to csv by overwriting the file 
	with atomic_overwrite(filename) as f:
		df.to_csv(f, index = None)

	print('File saved with distributions')