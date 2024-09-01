import pandas as pd
import requests
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values
from app.utilities.responses import AlphaVantageAPIKey

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)


class AlphaVantage:
    def __init__(self, symbol):
        self.api_key = Alpha_vintage_key
        self.symbol = symbol
        self.url = f'https://www.alphavantage.co/query?function='

    async def balance_sheet(self):
        url = self.url + f'=BALANCE_SHEET&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()

        return pd.DataFrame(data)

    async def income_statement(self):
        url = self.url + f'INCOME_STATEMENT&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()

        return pd.DataFrame(data)

    async def cash_flows(self):
        url = self.url + f'CASH_FLOW&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()

        annual_reports = data.get('annualReports')
        return pd.DataFrame(annual_reports)

    async def company_price_to_earnings_ratio(self):
        url = self.url + f'EARNINGS&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()

        return pd.DataFrame(data.get('annualEarnings', []))

    async def company_overview(self):
        url = self.url + f'OVERVIEW&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def company_annual_earnings_per_share(self):
        url = self.url + f'EARNINGS&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return pd.DataFrame(data.get('annualEarnings', []))

    async def stock_minutes(self, minutes: int):
        url = self.url + f'TIME_SERIES_INTRADAY&symbol={self.symbol}&interval={minutes}min&apikey={self.api_key}'

        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def stock_days(self):
        url = self.url + f'TIME_SERIES_DAILY&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def stock_weeks(self):
        url = self.url + f'TIME_SERIES_WEEKLY&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def stock_months(self):
        url = self.url + f'TIME_SERIES_MONTHLY&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def stock_monthly_adjusted(self):
        url = self.url + f'TIME_SERIES_MONTHLY_ADJUSTED&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return pd.DataFrame(data['Monthly Adjusted Time Series'])

    async def stock_latest(self):
        url = self.url + f'GLOBAL_QUOTE&symbol={self.symbol}&apikey={self.api_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return data

    async def news(self):
        url = self.url + f'NEWS_SENTIMENT&tickers={self.symbol}&apikey={Alpha_vintage_key}'
        data = requests.get(url).json()

        if 'Information' in data:
            raise AlphaVantageAPIKey()
        return pd.DataFrame(data['feed'])
