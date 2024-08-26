from app.models.base_models.stock_calculator import StockCalculator


class FairValue(StockCalculator):

    def __init__(self,earnings_per_share_growth_rate, dividend_yield, price_to_earnings_ratio):
        self.earnings_per_share_growth_rate = float(earnings_per_share_growth_rate)
        self.dividend_yield = float(dividend_yield)
        self.price_to_earnings_ratio = float(price_to_earnings_ratio)

    def calculate(self):
        return (self.earnings_per_share_growth_rate + self.dividend_yield) / self.price_to_earnings_ratio
