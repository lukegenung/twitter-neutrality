# twitter-sentiment-bot
Real-time sentiment analysis of Twitter data using NLTK and Google Sheets as a database.

This NLP framework does the following:
1. Build a sentiment analysis model using NLTK twitter_samples and any additional training samples provided by the user
2. Read new Twitter data from a Google Sheet
3. Processes and scores sentiment of the new Twitter data
4. Posts the processed data back to a Google Sheet

Google Sheets is used to automate querying Twitter API on a scheduled basis. Both raw and processed data is stored in Google Sheets.
