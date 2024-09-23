import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError

class TaxRate(StockCalculator):

    def __init__(self, income_statement):
        self.income_statement = income_statement

    async def calculate(self):
        try:

            tax_provision = self.income_statement.loc['Tax Provision']
            pretax_income = self.income_statement.loc['Pretax Income']

            tax_rate = (tax_provision / pretax_income) * 100
            tax_rate = tax_rate.round(2).dropna()

            return tax_rate
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
