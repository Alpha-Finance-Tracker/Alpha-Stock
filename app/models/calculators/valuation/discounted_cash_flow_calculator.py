import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.models.calculators.terminal_value_calculator import TerminalValue
from app.utilities.responses import CalculationError


class DiscountedCashFlow(StockCalculator):

    def __init__(self, cash_flow, discount_rate):
        self.cash_flow = cash_flow
        self.discount_rate = discount_rate if discount_rate > 0.03 else 0.04
        self.terminal_value = None

    @property
    def terminal_growth_rate(self):
        return 0.03  # Hardcoded for now

    @property
    def projection_years(self):
        return 10  # Hardcoded for now

    @property
    def last_year_free_cash_flow(self):
        return float(self.cash_flow.loc['Free Cash Flow'][0])

    async def calculate(self):

        try:
            latest_cash_flow = self.last_year_free_cash_flow

            self.terminal_value = await TerminalValue(latest_cash_flow, self.terminal_growth_rate,
                                                      self.discount_rate).calculate()

            return (sum([
                (latest_cash_flow / (1 + self.discount_rate) ** year) for year in range(1, self.projection_years + 1)])
                    + (self.terminal_value / (1 + self.discount_rate) ** self.projection_years))
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
