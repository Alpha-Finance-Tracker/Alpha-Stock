import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class TaxRate(StockCalculator):

    def __init__(self, income_statement):

        self.income_statement = income_statement


    @property
    def last_year_income_tax_expense(self):
        return float(self.income_statement['incomeTaxExpense'].iloc[0])

    @property
    def last_year_income_before_tax(self):
        return float(self.income_statement['incomeBeforeTax'].iloc[0])
    async def calculate(self):
        try:
            return self.last_year_income_tax_expense / self.last_year_income_before_tax
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
