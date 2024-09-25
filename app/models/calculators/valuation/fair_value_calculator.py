import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.responses import CalculationError


class FairValue(StockCalculator):  # Peter Lynch Calculator

    def __init__(self, yahoo_finance):
        self.yahoo_finance = yahoo_finance

    async def calculate(self):
        try:
            price_to_earnings_ratio = float(self.yahoo_finance.info['forwardPE'])
            dividend_yield = float(self.yahoo_finance.info['dividendYield']) * 100
            growth_estimates = self.yahoo_finance.growth_estimates.iloc[4]
            earnings_per_share_growth_rate = (growth_estimates['index'] if growth_estimates['stock'] == 0.0 else growth_estimates['stock']) * 100

            print(price_to_earnings_ratio)
            print(dividend_yield)
            print(earnings_per_share_growth_rate)

            return (earnings_per_share_growth_rate + dividend_yield) / price_to_earnings_ratio

        except (ZeroDivisionError, ValueError, TypeError,KeyError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
