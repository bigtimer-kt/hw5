import json
# Buy if price < 98% of 5 -day avg
# Sell if price > 102% of 5-day average
def meanReversionStrategy(prices):
    window = 5  #5 day moving avg
    holdings = []
    profit = 0.0
    first_buy = None  # Needed to calc percent return

    print("\nMean Reversion Strategy Output:")
    for i in range(window, len(prices)):
        avg = sum(prices[i - window:i]) / window  # Calc 5-day average
        price = prices[i]

        if price < avg * 0.98: # Buy
            holdings.append(price)
            if first_buy is None:
                first_buy = price
            print(f"buying at: {price}")
        elif price > avg * 1.02 and holdings: # Sell
            buy_price = holdings.pop(0)
            trade_profit = price - buy_price
            profit += trade_profit
            print(f"selling at: {price}")
            print(f"trade profit: {round(trade_profit, 2)}")
#calc return as %
    returns = (profit / first_buy * 100) if first_buy else 0
    print(f"Total profit: {round(profit, 2)}")
    print(f"Percent return: {round(returns, 2)}")
    return round(profit, 2), round(returns, 2)

#Simple mov avg
# Buy if price > avg
# Sell if price < avg
def simpleMovingAverageStrategy(prices):
    window = 5
    holdings = []
    profit = 0.0
    first_buy = None

    print("\nSimple Moving Average Strategy Output:")
    for i in range(window, len(prices)):
        avg = sum(prices[i - window:i]) / window
        price = prices[i]

        if price > avg: #buy
            holdings.append(price)
            if first_buy is None:
                first_buy = price
            print(f"buying at: {price}")
        elif price < avg and holdings: #sell
            buy_price = holdings.pop(0)
            trade_profit = price - buy_price
            profit += trade_profit
            print(f"selling at: {price}")
            print(f"trade profit: {round(trade_profit, 2)}")

    returns = (profit / first_buy * 100) if first_buy else 0
    print(f"Total profit: {round(profit, 2)}")
    print(f"Percent return: {round(returns, 2)}")
    return round(profit, 2), round(returns, 2)

# save results to results.json
def saveResults(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

# 10 stocks
tickers = ['AAPL', 'GOOG', 'ADBE', 'TSLA', 'MSFT', 'AMZN', 'META', 'NVDA', 'NFLX', 'INTC']
results = {}
# loop through each stock
for ticker in tickers:
    with open(f"{ticker}.txt") as file:
        lines = file.readlines()
        prices = [round(float(line.strip()), 2) for line in lines]
        results[f"{ticker}_prices"] = prices
        #this stuff still mega confusing
        print(f"\n=== {ticker} Simple Moving Average Strategy ===")
        sma_profit, sma_return = simpleMovingAverageStrategy(prices)
        results[f"{ticker}_sma_profit"] = sma_profit
        results[f"{ticker}_sma_returns"] = sma_return
        # record the results
        print(f"\n=== {ticker} Mean Reversion Strategy ===")
        mr_profit, mr_return = meanReversionStrategy(prices)
        results[f"{ticker}_mr_profit"] = mr_profit
        results[f"{ticker}_mr_returns"] = mr_return
# save to JSON
saveResults(results)
print("\n Results saved to results.json")
