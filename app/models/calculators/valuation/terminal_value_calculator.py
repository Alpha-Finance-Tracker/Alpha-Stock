import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class TerminalValue(StockCalculator):

    def __init__(self, latest_cash_flow, discount_rate):
        self.latest_cash_flow = latest_cash_flow
        self.discount_rate = discount_rate
        self.terminal_growth_rate = 0.3

    async def calculate(self):
        try:
            return self.latest_cash_flow * (1 + self.terminal_growth_rate) / (
                    self.discount_rate - self.terminal_growth_rate)

        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
