import asyncio
import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.models.calculators.cost_of_debt_calculator import CostOfDebt
from app.models.calculators.cost_of_equity_calculator import CostOfEquity
from app.models.calculators.debt_ratio_calculator import DebtRatio
from app.models.calculators.equity_ratio_calculator import EquityRatio
from app.models.calculators.market_data_calculator import AverageMarketData
from app.models.calculators.tax_rate_calculator import TaxRate
from app.models.calculators.total_market_value_calculator import TotalMarketValue
from app.utilities.responses import CalculationError


class DiscountRate(StockCalculator):

    def __init__(self, income_statement, balance_sheet, company_overview, market_data, stock_info):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.company_overview = company_overview
        self.market_data = market_data
        self.stock_info = stock_info

    @property
    def risk_rate(self):
        return 0.03

    @property
    def beta(self):
        try:
            return self.stock_info['beta']
        except KeyError:
            try:
                return self.company_overview['Beta']
            except KeyError:
                return 1

    async def calculate(self):

        try:
            avg_market_value, tax_rate, cost_of_debt = await asyncio.gather(
                AverageMarketData(self.market_data).calculate(),
                TaxRate(self.income_statement).calculate(),
                CostOfDebt(self.income_statement, self.balance_sheet).calculate(),
                return_exceptions=True
            )

            cost_of_equity = await CostOfEquity(avg_market_value, self.risk_rate, self.beta).calculate()
            debt_ratio = await DebtRatio(self.balance_sheet).calculate()
            equity_ratio = await EquityRatio(self.balance_sheet).calculate()
            total_market_value = await TotalMarketValue(equity_ratio, debt_ratio).calculate()

            weighted_average_cost_of_capital = (
                    (equity_ratio / total_market_value) * cost_of_equity
                    + (debt_ratio / total_market_value) * cost_of_debt * (1 - tax_rate)
            )

            return weighted_average_cost_of_capital
        except (ZeroDivisionError, ValueError,TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()

