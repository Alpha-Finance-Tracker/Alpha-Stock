from app.models.base_models.stock_calculator import StockCalculator


class TerminalValue(StockCalculator):

    def __init__(self,latest_cash_flow,terminal_growth_rate,discount_rate):
        self.latest_cash_flow = latest_cash_flow
        self.terminal_growth_rate = terminal_growth_rate
        self.discount_rate = discount_rate


    async def calculate(self):
        try:
            return self.latest_cash_flow * (1 + self.terminal_growth_rate) / (
                    self.discount_rate - self.terminal_growth_rate)

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
