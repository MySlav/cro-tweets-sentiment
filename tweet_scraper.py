#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 12:20:58 2022

@authors: Mislav Spajić, Hrvoje Kopić

Prerequistes: twitter developer account
                - created project and app with keys and tokens
"""

import tweepy as tw
import pandas as pd
import re


def tweet_scraper(tweet):
    ID = tweet.id
    source = tweet.source
    text = tweet.full_text.replace('\n', ' ').replace('\r', ' ')
    user_name = tweet.user.screen_name
    user_location = tweet.user.location.replace('\n', ' ').replace('\r', ' ')
    acct_desc = tweet.user.description.replace('\n', ' ').replace('\r', ' ')
    following = tweet.user.friends_count
    followers = tweet.user.followers_count
    total_tweets = tweet.user.statuses_count
    user_created = tweet.user.created_at
    favourite_count = tweet.favorite_count
    retweet_count = tweet.retweet_count
    hashs = ["#" + hashtag["text"] for hashtag in tweet.entities['hashtags']]
    hashs = ', '.join(str(s) for s in hashs)
    lang = tweet.lang
    if tweet.place is not None:
        country = tweet.place.country
        country_code = tweet.place.country_code
        place_type = tweet.place.place_type
        full_name = tweet.place.full_name
        name = tweet.place.name
    else:
        country = None
        country_code = None
        place_type = None
        full_name = None
        name = None

    created_at = tweet.created_at

    line = {'id': ID, 'user_author': user_name, 'user_location': user_location,
            "user_source": source, 'user_description': acct_desc,
            'user_friends_count': following, 'user_followers': followers,
            'user_total_tweets': total_tweets, 'user_created': user_created,
            'general_lang': lang, 'general_created': created_at,
            'general_text': text, 'general_hashtags': hashs,
            'general_favorite_count': favourite_count,
            'general_retweet_count': retweet_count, 'place_country': country,
            'place_country_code': country_code, 'place_name': name,
            'place_full_name': full_name, 'place_place_type': place_type
            }

    return line


def split_it(strng):
    a = re.search(r'(?<=id=)(.*?)(?=&tweet_mode)', strng)
    if a:
        a = a.group(1)
    b = re.split(r'(?<=id=)(.*?)(?=&tweet_mode)', strng)[0]
    return pd.Series([a, b])


# Twitter API config
consumer_key = 'your_key_here'
consumer_secret = 'your_secret_here'
access_token = 'your_access_token_here'
access_token_secret = 'your_access_token_secret_here'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Source for Annotated tweets in Croatian
# https://www.clarin.si/repository/xmlui/handle/11356/1054

anot_tweet = pd.read_csv('Croatian_Twitter_sentiment.csv')
# anot.tweet.head(5)

# Loop for creating output
output = []
errors = []
for row in anot_tweet.iterrows():
    try:
        tweet = api.get_status(row[1][0], tweet_mode="extended")
        line = tweet_scraper(tweet)
        line["sentiment"] = row[1][1]
        line["anotator"] = row[1][2]
        output.append(line)
    except Exception as e:
        print("Tweepy Error: {}".format(e))
        errors.append("Tweepy Error: {}".format(e))
        pass
# Some data wrangling
tweet_output = pd.DataFrame(output)
tweet_errors = pd.DataFrame([error.split("\n") for error in errors],
                            columns=['0', '1'])


# Check error counts
tweet_errors['0'].value_counts()

# Cleaning up and saving ids that failed
temp = tweet_errors['0'].apply(split_it)
temp.columns = ['2', '3']
err = pd.concat([tweet_errors, temp], axis=1)
err['0'] = err['3']
err.drop(columns='3', inplace=True)

err['0'].value_counts()


# Only 118+65 failed that we could try to retry, but it is so small
# number so I don't think it is worth to write additional code

# Just to check if we have the right count
len(tweet_errors)+len(tweet_output) == len(anot_tweet)

# len(tweet_errors) len(tweet_output)
# Out[34]: 20999 Out[36]: 76292
# Output data
tweet_output.to_csv('tweet_output.csv', index=False)
