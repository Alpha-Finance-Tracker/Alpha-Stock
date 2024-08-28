from app.models.base_models.stock_calculator import StockCalculator


class RelativeValue(StockCalculator):

    def __init__(self, competitors_price_to_earnings_ratio_list):
        self.competitors_price_to_earnings_ratio_list = competitors_price_to_earnings_ratio_list


    def calculate(self):
        return sum(self.competitors_price_to_earnings_ratio_list) / len(self.competitors_price_to_earnings_ratio_list)
