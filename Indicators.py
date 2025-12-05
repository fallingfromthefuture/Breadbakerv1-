# indicators.py
def detect_bos(df):
    df = df.copy()
    df['bos_up'] = (df['high'] > df['high'].shift(1)) & (df['high'].shift(1) <= df['high'].shift(2))
    df['bos_down'] = (df['low'] < df['low'].shift(1)) & (df['low'].shift(1) >= df['low'].shift(2))
    return df

def detect_ob_fvg(df, lookback=20):
    df = df.copy()
    df['fvg_up'] = (df['low'] > df['high'].shift(2)) & (df['low'].shift(1) > df['high'].shift(3))
    df['fvg_down'] = (df['high'] < df['low'].shift(2)) & (df['high'].shift(1) < df['low'].shift(3))
    return df
