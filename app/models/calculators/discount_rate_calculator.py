from app.models.base_models.stock_calculator import StockCalculator


class DiscountRate(StockCalculator):


    def __init__(self, risk_rate,market_return,beta,cost_of_debt,debt_ratio,equity_ratio,tax_rate):
        self.risk_rate = risk_rate
        self.market_return = market_return
        self.beta = beta
        self.cost_of_debt = cost_of_debt
        self.debt_ratio = debt_ratio
        self.equity_ratio = equity_ratio
        self.tax_rate = tax_rate
        self.total_market_value = self.equity_ratio + self.debt_ratio
        self.cost_of_equity = self.risk_rate + self.beta * (self.market_return - self.risk_rate)

    def calculate(self):
        weighted_average_cost_of_capital = \
            ((self.equity_ratio / self.total_market_value) * self.cost_of_equity)
        + (self.debt_ratio / self.total_market_value) * self.cost_of_debt * (1-self.tax_rate)

        return weighted_average_cost_of_capital
