from app.models.base_models.stock_calculator import StockCalculator


class DiscountedCashFlow(StockCalculator):

    def __init__(self, cash_flows, discount_rate):
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate

    def calculate(self):
        return (sum([
            (self.latest_cash_flow / (1 + self.discount_rate) ** year) for year in range(1, self.projection_years + 1)])
                + (self.terminal_value / (1 + self.discount_rate) ** self.projection_years))

    @property
    def latest_cash_flow(self):
        return self.cash_flows.loc['Free Cash Flow'][0]

    @property
    def terminal_growth_rate(self):
        return 0.03  # Hardcoded for now

    @property
    def projection_years(self):
        return 5  # Hardcoded for now

    @property
    def terminal_value(self):
        return self.latest_cash_flow * (1 + self.terminal_growth_rate) / (
                self.discount_rate - self.terminal_growth_rate)
