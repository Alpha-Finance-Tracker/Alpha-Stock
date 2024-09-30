from app.models.base_models.stock_calculator import StockCalculator


class DebtToEbitdaRatio(StockCalculator):

    def __init__(self, ebitda, total_debt):
        self.ebitda = ebitda
        self.total_debt = total_debt

    def __repr__(self):
        return (f"DebtToEbitdaRatio(ebitda={self.ebitda}, "
                f"total_debt={self.total_debt})")

    async def calculate(self):
        total_debt = self.total_debt / self.ebitda
        total_debt = total_debt.round(2).dropna()
        return total_debt
