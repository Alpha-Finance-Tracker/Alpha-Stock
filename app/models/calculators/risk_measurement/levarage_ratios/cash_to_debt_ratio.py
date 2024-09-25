from app.models.base_models.stock_calculator import StockCalculator


class CashToDebtRatio(StockCalculator):

    def __init__(self,total_debt,cash_and_cash_equivalents):
        self.total_debt=total_debt
        self.cash_and_cash_equivalents=cash_and_cash_equivalents

    async def calculate(self):
        cash_to_debt = (self.cash_and_cash_equivalents / self.total_debt)
        cash_to_debt =cash_to_debt.round(2).dropna()
        return cash_to_debt
