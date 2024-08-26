from app.models.base_models.stock_calculator import StockCalculator


class DiscountedCashFlow(StockCalculator):

    def __init__(self,free_cash_flow, discount_rate,terminal_growth_rate,projection_years):
        self.free_cash_flow = free_cash_flow
        self.discount_rate = discount_rate
        self.terminal_growth_rate = terminal_growth_rate
        self.projection_years = projection_years
        self.terminal_value = self.free_cash_flow * (1 + self.terminal_growth_rate) / (self.discount_rate - self.terminal_growth_rate)

    def calculate(self):
        return (sum([
            (self.free_cash_flow / (1 + self.discount_rate) ** year) for year in range(1, self.projection_years + 1)])
                   + (self.terminal_value / (1 + self.discount_rate) ** self.projection_years))
