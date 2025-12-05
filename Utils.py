# utils.py
import pandas as pd

def resample_df(df, timeframe):
    rule = {'1m':'1T','3m':'3T','5m':'5T','15m':'15T','1h':'1H'}.get(timeframe, '1T')
    return df.resample(rule).agg({
        'open':'first','high':'max','low':'min','close':'last','volume':'sum'
    }).dropna()

def atr(df, period=14):
    tr = pd.concat([
        df['high'] - df['low'],
        abs(df['high'] - df['close'].shift()),
        abs(df['low'] - df['close'].shift())
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()
