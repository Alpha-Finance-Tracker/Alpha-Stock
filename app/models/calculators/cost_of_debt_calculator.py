import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class CostOfDebt(StockCalculator):

    def __init__(self, income_statement, balance_sheet):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet

    @property
    def last_year_interest_expense(self):
        return float(self.income_statement['interestExpense'].iloc[0])

    @property
    def last_year_total_liabilities(self):
        return float(self.balance_sheet['totalLiabilities'].iloc[0])

    async def calculate(self):
        try:
            return self.last_year_interest_expense / self.last_year_total_liabilities
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
