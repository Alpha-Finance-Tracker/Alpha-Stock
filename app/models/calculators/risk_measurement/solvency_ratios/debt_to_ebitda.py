from app.models.base_models.stock_calculator import StockCalculator


class DebtToEbitda(StockCalculator):


    def __init__(self,ebitda,total_debt):
        self.ebitda=ebitda
        self.total_debt=total_debt
    async def calculate(self):
        return self.total_debt / self.ebitda
