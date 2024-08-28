import yfinance as yf
import pandas as pd


class YahooFinance:

    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_data = yf.Ticker(symbol)

    @property
    def market_data(self):
        market_data = yf.download(f'{self.symbol}')
        return market_data

    @property
    def cash_flow(self):
        cash_flow = self.stock_data.cash_flow.infer_objects(copy=False).fillna(0)
        return pd.DataFrame(cash_flow)

    @property
    def info(self):
        return self.stock_data.info

    @property
    def growth_estimates(self):
        return pd.DataFrame(self.stock_data.growth_estimates).dropna(axis=1)

    @property
    def major_holders(self):
        return self.stock_data.major_holders

    @property
    def insider_purchases(self):
        return self.stock_data.insider_purchases

    @property
    def institutional_holders(self):
        return self.stock_data.institutional_holders

    @property
    def insider_roster_holders(self):
        return self.stock_data.insider_roster_holders

    @property
    def financials(self):
        return self.stock_data.financials

    @property
    def income_statement(self):
        return self.stock_data.income_stmt

    @property
    def balance_sheet(self):
        return self.stock_data.balance_sheet

    @property
    def news(self):
        return self.stock_data.news

    @property
    def analyst_price_targets(self):
        return self.stock_data.analyst_price_targets

    @property
    def dividends(self):
        return pd.DataFrame(self.stock_data.dividends).dropna(axis=1)

    @property
    def splits(self):
        return pd.DataFrame(self.stock_data.splits).dropna(axis=1)
