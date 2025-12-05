# strategy.py
from utils import resample_df, atr
from indicators import detect_bos, detect_ob_fvg

class SMCStrategy:
    def __init__(self, params):
        self.p = params

    async def signal(self, df_1m):
        df_1h = resample_df(df_1m, '1h')
        df_15m = resample_df(df_1m, '15m')
        df_5m = resample_df(df_1m, '5m')
        df_3m = resample_df(df_1m, '3m')

        # 1h bias
        df_1h = detect_bos(df_1h)
        bull_bias = df_1h['bos_up'].iloc[-1]

        # 5m/15m OB + FVG
        df_5m = detect_ob_fvg(df_5m)
        fvg_touch = df_5m['fvg_up'].iloc[-1] or df_5m['fvg_down'].iloc[-1]

        # 3m/1m confirmation
        engulf_3m = df_3m['close'].iloc[-1] > df_3m['open'].iloc[-1]
        engulf_1m = df_1m['close'].iloc[-1] > df_1m['open'].iloc[-1]

        long = bull_bias and fvg_touch and engulf_3m and engulf_1m
        return 1 if long else -1 if not bull_bias else 0
