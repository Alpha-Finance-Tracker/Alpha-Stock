import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError

class TaxRate(StockCalculator):

    def __init__(self, income_before_tax,income_after_tax):
        self.income_before_tax = income_before_tax
        self.income_after_tax=income_after_tax

    def __repr__(self):
        return (f"TaxRate(income_before_tax={self.income_before_tax}, "
                f"income_after_tax={self.income_after_tax})")

    async def calculate(self):
        try:

            tax_rate = (self.income_after_tax / self.income_before_tax) * 100
            tax_rate = tax_rate.round(2).dropna()

            return tax_rate
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()


