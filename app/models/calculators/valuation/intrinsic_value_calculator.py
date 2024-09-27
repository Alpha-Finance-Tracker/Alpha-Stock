import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class IntrinsicValue(StockCalculator):
    def __init__(self,discounted_cash_flow,shares_outstanding):
        self.discounted_cash_flow = discounted_cash_flow
        self.shares_outstanding = shares_outstanding

    async def calculate(self):
        try:
            return round(self.discounted_cash_flow / float(self.shares_outstanding),2)
        except (ZeroDivisionError,ValueError,TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
