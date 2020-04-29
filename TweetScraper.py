import csv
import tweepy
import re

import twitter_credentials

def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    # create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
    api = tweepy.API(auth)

    # get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    # open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'wb') as file:
        w = csv.writer(file)

        # write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username','retweet_count','favorite_count','all_hashtags','followers_count','is_retweet'])

        # for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase,
                                   lang="en", tweet_mode='extended').items(1000):
            if 'retweeted_status' in dir(tweet): # check if retweet to print full text
                tweet_text = tweet.retweeted_status.full_text.encode('utf-8',errors='ignore')
                is_retweet = True
            else:
                tweet_text = tweet.full_text.encode('utf-8',errors='ignore')
                is_retweet = False

            w.writerow([tweet.created_at, tweet_text,
                        tweet.user.screen_name.encode('utf-8',errors='ignore'), tweet.retweet_count, tweet.favorite_count,
                        [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count, is_retweet])


consumer_key = twitter_credentials.CONSUMER_KEY
consumer_secret = twitter_credentials.CONSUMER_SECRET
access_token = twitter_credentials.ACCESS_TOKEN
access_token_secret = twitter_credentials.ACCESS_TOKEN_SECRET

hashtag_phrase = raw_input('Hashtag Phrase ')

if __name__ == '__main__':
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)

