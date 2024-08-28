from app.models.base_models.stock_calculator import StockCalculator
from app.models.calculators.cost_of_debt_calculator import CostOfDebt
from app.models.calculators.debt_ratio_calculator import DebtRatio
from app.models.calculators.equity_ratio_calculator import EquityRatio
from app.models.calculators.market_data_calculator import AverageMarketData
from app.models.calculators.tax_rate_calculator import TaxRate


class DiscountRate(StockCalculator):

    def __init__(self, income_statement, balance_sheet, company_overview, market_data, stock_info):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.company_overview = company_overview
        self.market_data = market_data
        self.stock_info = stock_info

    def calculate(self):
        weighted_average_cost_of_capital = (
                (self.equity_ratio / self.total_market_value) * self.cost_of_equity
                + (self.debt_ratio / self.total_market_value) * self.cost_of_debt * (1 - self.tax_rate)
        )

        return weighted_average_cost_of_capital

    @property
    def risk_rate(self):
        return 0.03  # Hardcoded value for now

    @property
    def average_market_value(self):
        return AverageMarketData(self.market_data).calculate()

    @property
    def beta(self):
        return self.stock_info['beta'] or self.company_overview['Beta'] or 1

    @property
    def cost_of_debt(self):
        return CostOfDebt(self.income_statement, self.balance_sheet).calculate()

    @property
    def debt_ratio(self):
        return DebtRatio(self.balance_sheet).calculate()

    @property
    def equity_ratio(self):
        return EquityRatio(self.balance_sheet).calculate()

    @property
    def tax_rate(self):
        return TaxRate(self.income_statement).calculate()

    @property
    def cost_of_equity(self):
        return self.risk_rate + self.beta * (self.average_market_value - self.risk_rate)

    @property
    def total_market_value(self):
        return self.equity_ratio + self.debt_ratio
