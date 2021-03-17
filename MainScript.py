import time
import BinanceScript
import Config
import TwitterScript

# Buy
# Sell
# Cancel
# LimitSell
# LimitBuy

tweet_history = []
while True:
    new_tweets = []
    new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
    if len(new_tweets) > 0:
        #  Start a binance transaction
        print("Buying doge coin")
    time.sleep(2)


