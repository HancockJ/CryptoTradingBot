import time
import BinanceScript
import Config
import TwitterScript


def create_transaction():
    # Get doge value @ start of transaction
    start_price = 10
    # Buy Doge
    # Wait X time
    time.sleep(5)
    # Sell Doge
    #BinanceScript.sell_order("ETHUSDT", "5")
    # Get doge price @ end of transaction
    end_price = 11
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
