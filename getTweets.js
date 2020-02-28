// Send queries to Twitter Search API to get tweet data.

/**
 * Enter a query in the GetTweets sheet and hit the button to send a query to the Twitter API.
 */
function getTweetsButton() {
  // Set variables for GetTweets sheet.
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var query = sheet.getRange("GetTweets!B3").getValue().toString();
  var lang = sheet.getRange("GetTweets!C3").getValue().toString();
  var resultType = sheet.getRange("GetTweets!D3").getValue().toString();
  var count = sheet.getRange("GetTweets!E3").getValue();
  var tweetMode = sheet.getRange("GetTweets!F3").getValue().toString();

  // Set variables for TweetLog sheet.
  var logsheet = sheet.getSheetByName("TweetLog");
  var row = 2
  var col = 2
  var lastLogRow = logsheet.getLastRow();
  var idArray = logsheet.getRange(row, col, lastLogRow).getValues();
  var sinceID = Math.max.apply(null, idArray);

  Logger.log('Fetching tweets after since_id: ' + sinceID)

  // Check if any required parameters are missing.
  var err = sheet.getRange("GetTweets!G3").getValue();
  if (err) {
    sheet.msgBox(err);
  } else {
    getTweets(query, lang, resultType, count, tweetMode, sinceID);
  }
}


/**
 * Get tweets by sending queries to the Twitter API Search endpoint.
 * Will only get Tweets created more recently than Tweets that are already logged.
 *
 * @param {string} query Twitter search query as string (500 characters max).
 * Include multiple values using '+AND+' or '+OR+'. Ex: 'apples+AND+orangutans'.
 * @param {string} lang Restricts tweets to the given language.
 * @param {string} resultType Specifies type of search results to receive.
 * Options are recent, popular or mixed.
 * @param {integer} count The number of tweets to return, up to a maximum of 100.
 * @param {string} tweetMode Specifies whether to limit Tweet information to 140 characters.
 * @param {integer} sinceID Tweet ID of the most recently created Tweet in TweetLog sheet.
 */
function getTweets(query, lang, resultType, count, tweetMode, sinceID) {

  // Get the Twitter request headers.
  var requestHeaders = getRequestHeaders()

  // Set the request URL.
  var requestUrl = 'https://api.twitter.com/1.1/search/tweets.json'
  var params = 
    '?q=' + query + 
    '&lang=' + lang + 
    '&result_type=' + resultType +
    '&count=' + count +
    '&tweet_mode=' + tweetMode
    // ADD sinceID !!!
  var request = requestUrl + params
  Logger.log('Request URL: ' + request);

  // Get the response from Twitter Search API.  
  try {
    var response = UrlFetchApp.fetch(request, requestHeaders);
  } catch (e) {
    Logger.log("Error: " + e);
  }

  // Parse the tweets.
  var tweets = JSON.parse(response.getContentText());
  Logger.log('# of tweets fetched: ' + tweets.statuses.length);

  // Write the tweets to TweetLog sheet.
  logTweets(tweets);
}


/**
  * Get an access token and API request headers.
  * Ensure that your Twitter credentials are populated below.
*/
function getRequestHeaders() {
  // Set the consumer key and secret - ENTER YOUR CREDENTIALS!
  var consumerKey = 'hkdqDF8JCrCLxeKg4jZ5ZeJY1';
  var consumerSecret = 'x4ipkG36yEJh7hIBRZczU8DCeNDFbQMpzWLdmyPGR3KfuDPUXN';

  // Get access token.
  var tokenUrl = "https://api.twitter.com/oauth2/token";
  var tokenCredential = Utilities.base64EncodeWebSafe(consumerKey + ":" + consumerSecret);
  var tokenOptions = {
    headers : {
      Authorization: "Basic " + tokenCredential,
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    },
    method: "post",
    payload: "grant_type=client_credentials"
  };  
  var responseToken = UrlFetchApp.fetch(tokenUrl, tokenOptions);
  var parsedToken = JSON.parse(responseToken);
  var token = parsedToken.access_token;

  // Return the request headers.
  var apiOptions = {
    headers : {
      Authorization: 'Bearer ' + token
    },
    "method" : "get"
  };

  return apiOptions;
}


/**
  * Write tweet data to TweetLog sheet.
  *
  * @param {array} tweets Object of all tweet information fetched from Twitter API.
*/
function logTweets(tweets) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var logsheet = sheet.getSheetByName("TweetLog");
  var retweetCount = 0
  Logger.log('Initiated logging!');

  // Log each tweet in the TweetLog sheet.
  for (var i = 0; i < tweets.statuses.length; i++) {
    // Skip and do not log retweets.
    if (tweets.statuses[i].retweeted_status != undefined) {
      retweetCount++
      continue;
    }
    
    var lastLogRow = logsheet.getLastRow();
    var createdAt = tweets.statuses[i].created_at;
    var tweetID = tweets.statuses[i].id;
    var screenName = tweets.statuses[i].user.screen_name;
    var fullText = tweets.statuses[i].full_text;

    logsheet.getRange(lastLogRow + 1, 1).setValue([createdAt]);
    logsheet.getRange(lastLogRow + 1, 2).setValue([tweetID]);
    logsheet.getRange(lastLogRow + 1, 3).setValue([screenName]);
    logsheet.getRange(lastLogRow + 1, 4).setValue([fullText]);
  }

  Logger.log('# of retweets removed: ' + retweetCount);
  Logger.log('# of tweets logged: ' + (tweets.statuses.length - retweetCount))
}