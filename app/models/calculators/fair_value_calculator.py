from app.models.base_models.stock_calculator import StockCalculator
from app.models.data_stream.yahoo_finance_data import YahooFinance


class FairValue(StockCalculator): # Peter Lynch Calculator

    def __init__(self,symbol):
        self.symbol = symbol
        self.yahoo_finance = YahooFinance(self.symbol)


    def calculate(self):
        price_to_earnings_ratio = float(self.yahoo_finance.info['forwardPE'])
        dividend_yield = float(self.yahoo_finance.info['dividendYield'])
        earnings_per_share_growth_rate = float(self.yahoo_finance.growth_estimates.iloc[4])

        return (earnings_per_share_growth_rate + dividend_yield) / price_to_earnings_ratio
