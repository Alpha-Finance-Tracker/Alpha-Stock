import yfinance as yf
import pandas as pd


class YahooFinance:

    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_data = yf.Ticker(symbol)
        self.x = None

    @property
    def cash_flow(self):
        return pd.DataFrame(self.stock_data.cash_flow).infer_objects(copy=False).fillna(0)
    @property
    def quarterly_cash_flow(self):
        return pd.DataFrame(self.stock_data.quarterly_cash_flow).fillna(0)

    @property
    def growth_estimates(self):
        return pd.DataFrame(self.stock_data.growth_estimates).fillna(0)

    @property
    def major_holders(self):
        return pd.DataFrame(self.stock_data.major_holders).fillna(0)

    @property
    def financials(self):
        return pd.DataFrame(self.stock_data.financials).fillna(0)

    @property
    def income_statement(self):
        return pd.DataFrame(self.stock_data.income_stmt).fillna(0)

    @property
    def quarterly_income_statement(self):
        return pd.DataFrame(self.stock_data.quarterly_income_stmt).fillna(0)

    @property
    def balance_sheet(self):
        return pd.DataFrame(self.stock_data.balance_sheet).fillna(0)

    @property
    def quarterly_balance_sheet(self):
        return pd.DataFrame(self.stock_data.quarterly_balance_sheet).fillna(0)

    @property
    def dividends(self):
        return pd.DataFrame(self.stock_data.dividends).dropna(axis=1)

    @property
    def splits(self):
        return pd.DataFrame(self.stock_data.splits).dropna(axis=1)

    @property
    def news(self):
        return pd.DataFrame(self.stock_data.news)

    @property
    def analyst_price_targets(self):
        return self.stock_data.analyst_price_targets

    @property
    def info(self):
        return self.stock_data.info

    @property
    def insider_purchases(self):
        return self.stock_data.insider_purchases  # Numpy.int64 error

    @property
    def institutional_holders(self):
        return self.stock_data.institutional_holders  # Numpy.int64 error

    @property
    def insider_roster_holders(self):
        return self.stock_data.insider_roster_holders  # Numpy.int64 error

    async def market_data(self):
        return yf.download(f'{self.symbol}')
