 # -*- coding: utf-8 -*- 

import os
from datetime import datetime
import tweepy

#ツイートメソッドを実装
def postTweet(content):
    consumer_key = '0nV97m31E0VKiEVdToOryKsvc' #os.environ["CONSUMER_KEY"]
    consumer_secret = '1xgJpn1v6l6y3VY9qHQtesDdkMotiTe8CCSiaX7QT3sSWNBpaY' #os.environ["CONSUMER_SECRET"]
    access_token_key = '897407941921218560-p4yMS4eRkrhWSntwDomLwnV0lVkoQNb' #os.environ["ACCESS_TOKEN_KEY"]
    access_token_secret = 'ETRg9GUS0FSdx3vh7GsSxNlZ26mn5koN8f8S0WzyMirtM' # os.environ["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)
	#ツイートを投稿
    api.update_status(content)

