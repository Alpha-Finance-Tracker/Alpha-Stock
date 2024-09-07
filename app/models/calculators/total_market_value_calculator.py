import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class TotalMarketValue(StockCalculator):

    def __init__(self, equity_ratio, debt_ratio):
        self.equity_ratio = equity_ratio
        self.debt_ratio = debt_ratio

    async def calculate(self):
        try:
            return self.equity_ratio + self.debt_ratio

        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
