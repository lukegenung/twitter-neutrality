'''
REQUIREMENTS:
1. Update the gsheet arguments below
2. The specified Google Sheet to pull from MUST have a column named 'status'

OPTIONAL:
1. If you want to add your own training data, update build_model.py
'''

import gsheet, build_model, sent_analysis, helpers
from nltk.tokenize import casual_tokenize
from nltk import classify

# Train a sentiment analysis model on stored twitter samples
classifier = build_model.main()

#### UDATE HERE: Put your workbook and sheet name
# Get new twitter data from a specified Google Sheet
tweets = gsheet.get_data(workbook_name="Tweet Logger", sheet_name="TweetLog")

# Score the sentiment of the new twitter data
tweets = sent_analysis.get_sentiment(classifier, tweets, keep_status=False)

#### UPDATE HERE: Put your workbook and sheet name
# Post the processed data to a new Google Sheet
gsheet.post_data(workbook_name="Tweet Analysis", sheet_name="ProcessedData", data=tweets)