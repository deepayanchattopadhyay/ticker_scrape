import pandas
import random
import string

# Create some test data (should look similar to yours)
tickers = ["AEFES", "AFYON", "AKBNK"] + [''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(68)]
dfs = {
    f"df_{timestamp.strftime('%H:%M:%S')}": pandas.DataFrame(
        [
            {
                "Ticker": ticker,
                "Last": random.randint(0, 50),
                "Bid": random.randint(0, 50),
                "Ask": random.randint(0, 50),
                "Other_1": random.randint(0, 50),
                "Other_2": random.randint(0, 50),
                "Other_3": random.randint(0, 50),
            }
            for ticker in tickers
        ]
    ).set_index("Ticker")
    for timestamp in pandas.date_range("2020-01-01", periods=100, freq="5min")
}

# Combine all dataframes into a single dataframe
df = pandas.concat([df.unstack().rename(key) for key, df in dfs.items()], axis=1).T

# Take the rolling mean (= moving average) over 6 periods (= 1/2 hour)
moving_averages = df.rolling(6).mean()