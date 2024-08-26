from app.models.base_models.stock_calculator import StockCalculator


class RelativeValue(StockCalculator):

    def __init__(self, competitors_price_to_earnings_ratio,number_of_competitors):
        self.competitors_price_to_earnings_ratio = competitors_price_to_earnings_ratio
        self.number_of_competitors = number_of_competitors

    def calculate(self):
        return self.competitors_price_to_earnings_ratio // self.number_of_competitors
