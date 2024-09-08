import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.responses import CalculationError


class FairValue(StockCalculator):  # Peter Lynch Calculator

    def __init__(self, symbol):
        self.symbol = symbol
        self.yahoo_finance = YahooFinance(self.symbol)

    @property
    def price_to_earnings_ratio(self):
        return float(self.yahoo_finance.info['forwardPE'])

    @property
    def dividend_yield(self):
        return float(self.yahoo_finance.info['dividendYield'])

    @property
    def earnings_per_share_growth_rate(self):
        growth_estimates = self.yahoo_finance.growth_estimates.iloc[4]

        return float(
            growth_estimates['index'] if growth_estimates['stock'] == 0.0 else growth_estimates['stock'])

    async def calculate(self):
        try:

            return (self.earnings_per_share_growth_rate + self.dividend_yield) / self.price_to_earnings_ratio
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
