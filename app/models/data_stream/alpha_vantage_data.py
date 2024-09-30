from functools import cache

import pandas as pd
import httpx
from dotenv import dotenv_values
from app.models.validators.alpha_vantage_validator import AlphaVantageValidator

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')


class AlphaVantage:
    def __init__(self, symbol):
        self.api_key = Alpha_vintage_key
        self.symbol = symbol
        self.url = 'https://www.alphavantage.co/query?function='

    def _fetch_data(self, endpoint):
        url = self.url + endpoint + f'&symbol={self.symbol}&apikey={self.api_key}'
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    @cache
    def balance_sheet(self):
        print(f'Fetching balance sheet')
        data = self._fetch_data('BALANCE_SHEET')
        AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    @cache
    def income_statement(self):
        print(f'Fetching income statement')
        data = self._fetch_data('INCOME_STATEMENT')
        AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    @cache
    def cash_flows(self):
        print(f'Fetching cash flows')
        data = self._fetch_data('CASH_FLOW')
        AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    @cache
    def company_overview(self):
        print(f'Fetching company overview')
        data = self._fetch_data('OVERVIEW')
        AlphaVantageValidator(data).validate()
        return data

    @cache
    def company_earnings(self):
        print(f'Fetching company earnings')
        data = self._fetch_data('EARNINGS')
        AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualEarnings'))

    @cache
    def news(self):
        print(f'Fetching news ')
        data = self._fetch_data(f'NEWS_SENTIMENT&tickers={self.symbol}')
        AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('feed'))
