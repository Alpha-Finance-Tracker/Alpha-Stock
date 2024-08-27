from app.models.base_models.stock_calculator import StockCalculator


class RelativeValue(StockCalculator):

    def __init__(self, competitors_price_to_earnings_ratio):
        self.competitors_price_to_earnings_ratio = sum(competitors_price_to_earnings_ratio)
        self.number_of_competitors = len(competitors_price_to_earnings_ratio)

    def calculate(self):
        return self.competitors_price_to_earnings_ratio // self.number_of_competitors
