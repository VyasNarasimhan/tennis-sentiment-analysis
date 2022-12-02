import requests
from dotenv import load_dotenv
import os
import json
from transformers import pipeline

class Tweet:
    def __init__(self):
        load_dotenv()
        self.BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
        self.url = 'https://api.twitter.com/2/tweets/search/recent'
        print(self.BEARER_TOKEN)

    def get_rating(self, player):
        data = self.get_tweets(player)
        print(data)
        sentiment_pipeline = pipeline('sentiment-analysis')
        sentiments = [sentiment_pipeline(tweet)[0] for tweet in data]
        return sum([-1 if sent['label'] == 'NEGATIVE' else 1 for sent in sentiments]) / len(sentiments)

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

    def get_tweets(self, player):
        data = json.loads(json.dumps(tweet.connect_to_endpoint({'query': player + ' lang:en'})))
        return [i['text'] for i in data['data']]

if __name__ == '__main__':
    tweet = Tweet()
    print(tweet.get_rating('casper ruud'))