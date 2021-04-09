import time
import BinanceScript
import Config
import TwitterScript
import math
import BinanceScript as binance


def make_transaction(asset):
    # Get input assets value @ start of transaction
    start_balance = float(binance.get_account_balance())
    print(f"BUYING {asset} With full account balance of: ${start_balance}")
    start_price = float(binance.getPrice(asset))

    units = math.floor(float(start_balance)/float(start_price))
    binance.buy_order(asset, units)

    sellPoint = .1
    start_time = time.time()
    elapsed_time = 0
    portion = math.floor(units * .25)
    print(units)
    while units >= portion:
        time.sleep(2)
        percent_change = ((float(binance.getPrice(asset)) - start_price) / start_price) * 100
        print("{:.3f}".format(percent_change))
        if percent_change > sellPoint:
            binance.sell_order(asset, portion)
            units = units - portion
            sellPoint += .005
            outputSell(percent_change, portion)
        elapsed_time = time.time() - start_time
        if elapsed_time > 86400:
            binance.sell_order(asset, units)
    if units > 0:
        binance.sell_order(asset, units)
        percent_change = ((float(binance.getPrice(asset)) - start_price) / start_price) * 100
        outputSell(percent_change, units)
    print(units)
    end_balance = float(binance.get_account_balance())
    # Output money made
    print(f"==> Transaction is over. You started with ${start_balance} and ended with ${end_balance}. Your total profit was"
          f" {float(end_balance) - float(start_balance)}.")


def outputSell(percent_change, portion):
    print(f"SOLD {portion} units for a P/L of {percent_change}%")


tweet_history = []
new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
while True:
    # new_tweets, tweet_history = TwitterScript.get_recent_tweets(Config, tweet_history)
    if len(new_tweets) > 0:
        print(new_tweets)
        #  Start a binance transaction
        make_transaction(Config.asset)
        new_tweets = []
    time.sleep(2)
