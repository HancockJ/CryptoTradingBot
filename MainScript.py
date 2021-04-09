import time
import BinanceScript
import Config
import TwitterScript
import math
import BinanceScript as binance


def make_transaction(asset):
    # Get input assets value @ start of transaction
    balance = binance.get_account_balance()
    print("Buying " + asset + " With full account balance of: " + balance)
    start_price = binance.getPrice(asset)
    # TODO: Buy Doge
    units = math.floor(float(balance)/float(start_price))
    buy = binance.buy_order(asset, units)

    time.sleep(20)  # TODO: Change to a function that calculates when we want to sell

    end_price = binance.getPrice(asset)
    sell = binance.sell_order(asset, units)

    # Output money made
    print(f"==> You bought Doge @ ${start_price} and sold doge @ ${end_price}. Your total profit was"
          f" {float(end_price) - float(start_price)}.")


tweet_history = []
while True:
    new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
    print(new_tweets)
    if len(new_tweets) > 0:
        #  Start a binance transaction
<<<<<<< HEAD
        make_transaction(Config.asset)
=======
        make_transaction("ETHUSDT")
>>>>>>> 0a8183df6018a7cd5f9d040f461ad9065e2bbcda
        new_tweets = 0
    time.sleep(2)
