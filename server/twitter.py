import requests
from dotenv import load_dotenv
import os
import json
from transformers import pipeline
from cleantext import clean

import time
import multiprocessing as mp

class Tweet:
    def __init__(self):
        load_dotenv()
        self.BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
        self.url = 'https://api.twitter.com/2/tweets/search/recent'

    def get_rating(self, tweet_list):
        sentiment_pipeline = pipeline('sentiment-analysis')
        sentiments = ([sentiment_pipeline(clean(tweet))[0] for tweet in tweet_list])
        rating = sum([sent['score'] * (-1 if sent['label'] == 'NEGATIVE' else 1) for sent in sentiments]) / len(sentiments)
        return rating / 2 + 5
        
    def bearer_oauth(self, r):
        r.headers["Authorization"] = f"Bearer {self.BEARER_TOKEN}"
        r.headers["User-Agent"] = "v2RecentSearchPytho"
        return r

    def connect_to_endpoint(self, query_params):
        response = requests.request("GET", self.url, auth=self.bearer_oauth, params=query_params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    
    def break_up_tweets(self, section_length, all_tweets):
        # create a list that contains lists of tweets
        tweet_list_2d = []
        
        # bounds to section of 1d list of tweets
        lower_bound = 0
        upper_bound = section_length
        
        # section the tweets and append each to tweet_list_2d
        while (upper_bound <= len(all_tweets)):
            tweet_list_2d.append(all_tweets[lower_bound:upper_bound])
            lower_bound += section_length
            upper_bound += section_length

        return tweet_list_2d

    def get_tweets(self, player):
        data = json.loads(json.dumps(tweet.connect_to_endpoint({'query': player + ' lang:en', 'tweet.fields': 'lang', 'max_results': 100})))
        raw_tweets = [i['text'] for i in data['data']]
        tweet_list_2d = self.break_up_tweets(10, raw_tweets)
        # return [i['text'] for i in data['data']]
        return tweet_list_2d

if __name__ == '__main__':
    tweet = Tweet()
    sectioned_tweets = tweet.get_tweets('novak djokovic')
    print(sectioned_tweets)
    for inner_tweets in sectioned_tweets:
        print(tweet.get_rating(inner_tweets))
