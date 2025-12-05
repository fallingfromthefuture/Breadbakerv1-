# exchange.py - Full async 2025
import ccxt.async_support as ccxt
import yaml, asyncio

with open('config.yaml') as f:
    config = yaml.safe_load(f)

class AsyncExchange:
    def __init__(self):
        name = config['exchange']
        if name == "hyperliquid":
            self.ex = ccxt.hyperliquid({
                'secret': config['hyperliquid']['private_key'],
                'enableRateLimit': True
            })
            if config['paper_trading']:
                self.ex.set_sandbox_mode(True)
        elif name == "drift":
            self.ex = ccxt.drift({
                'apiKey': config['drift']['api_key'],
                'secret': config['drift']['api_secret']
            })
        else:  # base / uniswap-style
            self.ex = ccxt.uniswap()
        self.symbol = config['symbol']
        self.position = None

    async def price(self):
        t = await self.ex.fetch_ticker(self.symbol)
        return t['last']

    async def balance(self):
        b = await self.ex.fetch_balance()
        return b.get('USDC', b['total'].get('USDC', 10000))

    async def market_order(self, side, amount):
        print(f"[LIVE] {side.upper()} {amount} {self.symbol}")
        return await self.ex.create_market_order(self.symbol, side, amount)

    async def close(self):
        await self.ex.close()
