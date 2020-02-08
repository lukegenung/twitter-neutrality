import build_model, get_sentiment

classifier = build_model.main()
tweet_filename = "2019_12_18_04_57_32.csv"
get_sentiment.main(classifier, tweet_filename)