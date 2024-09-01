import pandas as pd
import requests
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

from app.utilities.responses import AlphaVantageDailyLimitExceeded

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)


class AlphaVantage:
    def __init__(self, symbol):
        self.api_key = Alpha_vintage_key
        self.symbol = symbol

    async def balance_sheet(self):
        try:
            balance_sheet, _ = fd.get_balance_sheet_annual(self.symbol)
            return pd.DataFrame(balance_sheet)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def income_statement(self):
        try:
            income_statement, _ = fd.get_income_statement_annual(self.symbol)
            return pd.DataFrame(income_statement)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def cash_flows(self):
        try:
            url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.symbol}&apikey={self.api_key}'

            data = requests.get(url).json()
            annual_reports = data.get('annualReports')
            return pd.DataFrame(annual_reports)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def company_price_to_earnings_ratio(self):
        try:
            url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.symbol}&apikey={self.api_key}'

            data = requests.get(url).json()
            annual_earnings = data.get('annualEarnings', [])
            return pd.DataFrame(annual_earnings)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def company_overview(self):
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={self.api_key}'
            return requests.get(url).json()
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def company_annual_earnings_per_share(self):
        try:
            url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.symbol}&apikey={self.api_key}'
            data = requests.get(url).json()
            i = data.get('annualEarnings', [])
            return pd.DataFrame(i)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_minutes(self, minutes: int):
        try:
            url = (
                f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
                f'{self.symbol}&interval={minutes}min&apikey={self.api_key}')

            return requests.get(url).json()
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_days(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
                   f'{self.symbol}&apikey={self.api_key}')
            return requests.get(url).json()
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_weeks(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='
                   f'{self.symbol}&apikey={self.api_key}')
            return requests.get(url).json()
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_months(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='
                   f'{self.symbol}&apikey={self.api_key}')

            return requests.get(url)
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_monthly_adjusted(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol='
                   f'{self.symbol}&apikey={self.api_key}')

            data = requests.get(url).json()
            return pd.DataFrame(data['Monthly Adjusted Time Series'])
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def stock_latest(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
                   f'{self.symbol}&apikey={self.api_key}')

            return requests.get(url).json()
        except AlphaVantageDailyLimitExceeded as e:
            raise e

    async def news(self):
        try:
            url = (f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='
                   f'{self.symbol}&apikey={Alpha_vintage_key}')

            data = requests.get(url).json()
            return pd.DataFrame(data['feed'])
        except AlphaVantageDailyLimitExceeded as e:
            raise e
