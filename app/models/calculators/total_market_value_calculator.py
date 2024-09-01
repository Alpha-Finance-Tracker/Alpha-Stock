from app.models.base_models.stock_calculator import StockCalculator


class TotalMarketValue(StockCalculator):

    def __init__(self, equity_ratio, debt_ratio):
        self.equity_ratio = equity_ratio
        self.debt_ratio = debt_ratio

    async def calculate(self):
        try:
            return self.equity_ratio + self.debt_ratio

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
