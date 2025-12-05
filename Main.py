# main.py - ProFiT-SMC-Wyckoff Async Bot v3.1
import asyncio
import pandas as pd
from exchange import AsyncExchange
from strategy import SMCStrategy
from risk_manager import RiskManager
from utils import atr
from evolution import evolve

exchange = AsyncExchange()
strategy = SMCStrategy({})
position = None

async def fetch_1m():
    raw = await exchange.ex.fetch_ohlcv(exchange.symbol, '1m', limit=2000)
    df = pd.DataFrame(raw, columns=['ts','open','high','low','close','vol'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)
    return df

async def trading_loop():
    global position, strategy
    try:
        df = await fetch_1m()
        signal = await strategy.signal(df)
        price = await exchange.price()
        bal = await exchange.balance()
        atr_val = atr(df, 14).iloc[-1]

        rm = RiskManager(bal, price, atr_val)
        sl = price - atr_val * 1.5 if signal == 1 else price + atr_val * 1.5
        size = rm.position_size(sl)

        if signal == 1 and not position:
            await exchange.market_order('buy', size)
            position = {'side':'long', 'entry':price, 'size':size}
            print(f"ENTRY LONG @ {price}")

        elif signal == -1 and position and position['side']=='long':
            await exchange.market_order('sell', position['size'])
            position = None
            print(f"EXIT @ {price}")

    except Exception as e:
        print(f"Error: {e}")

async def daily_evolve():
    df = await fetch_1m()
    train, test = df.iloc[:len(df)//2], df.iloc[len(df)//2:]
    params = await evolve(train, test)
    global strategy
    strategy = SMCStrategy(params)

async def main():
    print("ProFiT-SMC-Wyckoff Async Bot v3.1 STARTED")
    print(f"Exchange: {config['exchange']} | Paper: {config.get('paper_trading',True)}")
    asyncio.create_task(daily_evolve())
    while True:
        await trading_loop()
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
