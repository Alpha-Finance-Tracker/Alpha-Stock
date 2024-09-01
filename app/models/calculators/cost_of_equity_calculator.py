from app.models.base_models.stock_calculator import StockCalculator


class CostOfEquity(StockCalculator):

    def __init__(self,average_market_return,risk_rate,beta):
        self.average_market_return = average_market_return
        self.risk_rate = risk_rate
        self.beta = beta

    async def calculate(self):
        try:
            return self.risk_rate + self.beta * (self.average_market_return - self.risk_rate)

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
