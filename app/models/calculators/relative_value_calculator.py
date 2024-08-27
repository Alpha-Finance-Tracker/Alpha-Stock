from app.models.base_models.stock_calculator import StockCalculator


class RelativeValue(StockCalculator):

    def __init__(self, competitors_price_to_earnings_ratio_list):
        self.competitors_price_to_earnings_ratio_list = competitors_price_to_earnings_ratio_list


    def calculate(self):
        competitors_price_to_earnings = [x for x in self.competitors_price_to_earnings_ratio_list if x is not None]
        return sum(competitors_price_to_earnings) / len(competitors_price_to_earnings)
