from app.models.base_models.stock_calculator import StockCalculator


class GrossProfitMargin(StockCalculator):

    def __init__(self, gross_profits, total_revenues):
        self.gross_profits = gross_profits
        self.total_revenues = total_revenues

    def __repr__(self):
        return (f"GrossProfitMargin(gross_profits={self.gross_profits}, "
                f"total_revenues={self.total_revenues})")

    async def calculate(self):
        gross_profit_margin = (self.gross_profits / self.total_revenues) * 100
        gross_profit_margin = gross_profit_margin.round(2).dropna()
        return gross_profit_margin
