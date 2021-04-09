import time
import BinanceScript
import Config
import TwitterScript
import BinanceScript as binance


def make_transaction(asset):
    # Get input assets value @ start of transaction
    start_price = binance.getPrice(asset)
    # TODO: Buy Doge
    buy = binance.buy_order("ETHUSDT", "2")

    time.sleep(20)  # TODO: Change to a function that calculates when we want to sell

    end_price = binance.getPrice(asset)
    # TODO: Sell Doge
    sell = binance.sell_order("ETHUSDT", "2")

    # Output money made
    print(f"==> You bought Doge @ ${start_price} and sold doge @ ${end_price}. Your total profit was"
          f" {float(end_price) - float(start_price)}.")


tweet_history = []
while True:
    new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
    print(new_tweets)
    if len(new_tweets) > 0:
        #  Start a binance transaction
        make_transaction()
        new_tweets = 0
    time.sleep(2)
