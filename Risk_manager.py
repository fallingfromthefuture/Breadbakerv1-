# risk_manager.py
import yaml
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)

class RiskManager:
    def __init__(self, balance, price, atr_val):
        self.balance = balance
        self.price = price
        self.atr = atr_val
        self.risk_pct = cfg['risk_percent_per_trade'] / 100

    def position_size(self, sl_price):
        risk_amount = self.balance * self.risk_pct
        distance = abs(self.price - sl_price)
        if distance == 0: return 0
        return round(risk_amount / distance, 6)

    def levels(self, entry, sl, side):
        risk = abs(entry - sl)
        tp1 = entry + risk if side == "buy" else entry - risk
        tp2 = entry + risk * 1.5 if side == "buy" else entry - risk * 1.5
        return {'sl': sl, 'tp1': tp1, 'tp2': tp2, 'risk': risk}
