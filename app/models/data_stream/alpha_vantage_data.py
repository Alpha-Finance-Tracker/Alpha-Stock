import pandas as pd
import requests
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)


class AlphaVantage:
    def __init__(self, symbol):
        self.api_key = Alpha_vintage_key
        self.symbol = symbol

    def balance_sheet(self):
        balance_sheet, _ = fd.get_balance_sheet_annual(self.symbol)
        return pd.DataFrame(balance_sheet)

    def income_statement(self):
        income_statement, _ = fd.get_income_statement_annual(self.symbol)
        return pd.DataFrame(income_statement)

    def cash_flows(self):
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()
        annual_reports = data.get('annualReports')
        return pd.DataFrame(annual_reports)

    def company_price_to_earnings_ratio(self):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()
        annual_earnings = data.get('annualEarnings', [])
        return pd.DataFrame(annual_earnings)

    def company_overview(self):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={self.api_key}'
        return requests.get(url).json()

    def company_annual_earnings_per_share(self):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()
        i = data.get('annualEarnings', [])
        return pd.DataFrame(i)

    def stock_minutes(self, minutes: int):
        url = (
            f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.symbol}&interval={minutes}min'
            f'&apikey={self.api_key}')
        return requests.get(url).json()

    def stock_days(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey={self.api_key}'
        return requests.get(url).json()

    def stock_weeks(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={self.symbol}&apikey={self.api_key}'
        return requests.get(url).json()

    def stock_months(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={self.symbol}&apikey={self.api_key}'
        return requests.get(url)

    def stock_monthly_adjusted(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()
        return pd.DataFrame(data['Monthly Adjusted Time Series'])

    def stock_latest(self):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={self.api_key}'
        return requests.get(url).json()

    def news(self):
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.symbol}&apikey={Alpha_vintage_key}'
        data = requests.get(url).json()
        return pd.DataFrame(data['feed'])
