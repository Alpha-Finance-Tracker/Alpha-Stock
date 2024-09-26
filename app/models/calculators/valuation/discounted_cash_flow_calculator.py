import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class DiscountedCashFlow(StockCalculator):

    def __init__(self, latest_cash_flow, discount_rate,terminal_value):
        self.latest_cash_flow = latest_cash_flow
        self.discount_rate = discount_rate
        self.terminal_value = terminal_value

    @property
    def projection_years(self):
        return 10  # Hardcoded for now

    async def calculate(self):

        try:
            return (sum([
                (self.latest_cash_flow / (1 + self.discount_rate) ** year) for year in range(1, self.projection_years + 1)])
                    + (self.terminal_value / (1 + self.discount_rate) ** self.projection_years))
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
