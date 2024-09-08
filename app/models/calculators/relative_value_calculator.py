import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class RelativeValue(StockCalculator):

    def __init__(self, competitors_price_to_earnings_ratio_list):
        self.competitors_price_to_earnings_ratio_list = competitors_price_to_earnings_ratio_list

    async def calculate(self):
        try:
            return (sum(self.competitors_price_to_earnings_ratio_list) /
                    len(self.competitors_price_to_earnings_ratio_list))
        except (ZeroDivisionError, ValueError, TypeError, IndexError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
