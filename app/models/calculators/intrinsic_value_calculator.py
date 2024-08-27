from app.models.base_models.stock_calculator import StockCalculator


class IntrinsicValue(StockCalculator):
    def __init__(self,discounted_cash_flow,shares_outstanding):
        self.discounted_cash_flow = discounted_cash_flow
        self.shares_outstanding = float(shares_outstanding)

    def calculate(self):
        return self.discounted_cash_flow / self.shares_outstanding
