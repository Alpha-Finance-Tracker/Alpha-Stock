from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class CashToDebtRatio(StockCalculator):

    def __init__(self, total_debt, cash_and_cash_equivalents):
        self.total_debt = total_debt
        self.cash_and_cash_equivalents = cash_and_cash_equivalents

    def __repr__(self):
        return (f"CashToDebtRatio(total_debt={self.total_debt}, "
                f"cash_and_cash_equivalents={self.cash_and_cash_equivalents})")

    async def calculate(self):
        try:
            cash_to_debt = (self.cash_and_cash_equivalents / self.total_debt)
            cash_to_debt = cash_to_debt.round(2).dropna()
            return cash_to_debt
        except:
            raise CalculationError()