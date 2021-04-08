import time
import BinanceScript
import Config
import TwitterScript
import BinanceScript as binance


def create_transaction():
    # Get doge value @ start of transaction
    start_price = binance.getPrice("Doge")
    # TODO: Buy Doge

    time.sleep(5)  # TODO: Change to a function that calculates when we want to sell

    end_price = binance.getPrice("Doge")
    # TODO: Sell Doge

    # Output money made
    print(f"==> You bought Doge @ ${start_price} and sold doge @ ${end_price}. Your total profit was"
          f" {end_price - start_price}.")


tweet_history = []
while True:
    new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
    print(new_tweets)
    if len(new_tweets) > 0:
        #  Start a binance transaction
        create_transaction()
    time.sleep(2)
