import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class CostOfEquity(StockCalculator):

    def __init__(self,average_market_return,risk_rate,beta):
        self.average_market_return = average_market_return
        self.risk_rate = risk_rate
        self.beta = beta

    async def calculate(self):
        try:
            return self.risk_rate + self.beta * (self.average_market_return - self.risk_rate)
        except (ValueError,TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
