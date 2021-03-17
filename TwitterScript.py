import json
import urllib.parse
import requests
from requests.auth import AuthBase
import time
import Config


class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'LabsRecentSearchQuickStartPython'})

        if response.status_code != 200:
            raise Exception("Cannot get a Bearer token (HTTP %d): %s" %
                            (response.status_code, response.text))

        body = response.json()
        return body['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
        r.headers['User-Agent'] = 'LabsRecentSearchQuickStartPython'
        return r


def get_recent_tweets(config, all_tweets):
    print("Getting new tweets...")
    headers = {
        "Accept-Encoding": "gzip"
    }
    query = urllib.parse.quote(f"from:{config.twitter_username} {config.tweet_keyword}")
    url = f"https://api.twitter.com/2/tweets/search/recent?max_results=10&query={query}"
    config.twitter_key_info["bearer_token"] = BearerTokenAuth(config.twitter_key_info["public"], config.twitter_key_info["private"])
    response = requests.get(url, auth=config.twitter_key_info["bearer_token"], headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: %s%s" %
                        (response.status_code, response.text))
    parsed = json.loads(response.text)
    #  Used for debugging
    #  pretty_print = json.dumps(parsed, indent=2, sort_keys=True)
    tweets = []
    if parsed["meta"]["result_count"] > 0:
        for tweet in parsed["data"]:
            if tweet["id"] not in all_tweets:
                print(tweet["text"])
                tweets.append(tweet["text"])
                all_tweets.append(tweet["id"])
    return tweets, all_tweets


tweet_history = []
while True:
    new_tweets, tweet_history = get_recent_tweets(Config, tweet_history)
    time.sleep(1)
