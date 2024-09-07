import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class EquityRatio(StockCalculator):

    def __init__(self, balance_sheet):

        self.balance_sheet = balance_sheet


    @property
    def last_year_total_liabilities(self):
        return float(self.balance_sheet['totalLiabilities'].iloc[0])

    @property
    def last_year_total_shareholder_equity(self):
        return float(self.balance_sheet['totalShareholderEquity'].iloc[0])

    async def calculate(self):
        try:
            total_liabilities = self.last_year_total_liabilities
            total_shareholder_equity = self.last_year_total_shareholder_equity

            return total_shareholder_equity / (total_liabilities + total_shareholder_equity)
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()