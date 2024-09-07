import pandas as pd
import httpx
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values
from app.models.validators.alpha_vantage_validator import AlphaVantageValidator
env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)


class AlphaVantage:
    def __init__(self, symbol):
        self.api_key = Alpha_vintage_key
        self.symbol = symbol
        self.url = 'https://www.alphavantage.co/query?function='

    async def _fetch_data(self, endpoint):
        url = self.url + endpoint + f'&symbol={self.symbol}&apikey={self.api_key}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def balance_sheet(self):
        data = await self._fetch_data('BALANCE_SHEET')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    async def income_statement(self):
        data = await self._fetch_data('INCOME_STATEMENT')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    async def cash_flows(self):
        data = await self._fetch_data('CASH_FLOW')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualReports'))

    async def company_overview(self):
        data = await self._fetch_data('OVERVIEW')
        await AlphaVantageValidator(data).validate()
        return data

    async def company_earnings(self):
        data = await self._fetch_data('EARNINGS')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('annualEarnings'))

    async def stock_minutes(self, minutes: int):
        data = await self._fetch_data(f'TIME_SERIES_INTRADAY&interval={minutes}min')
        await AlphaVantageValidator(data).validate()
        return data

    async def stock_days(self):
        data = await self._fetch_data('TIME_SERIES_DAILY')
        await AlphaVantageValidator(data).validate()
        return data

    async def stock_weeks(self):
        data = await self._fetch_data('TIME_SERIES_WEEKLY')
        await AlphaVantageValidator(data).validate()
        return data

    async def stock_months(self):
        data = await self._fetch_data('TIME_SERIES_MONTHLY')
        await AlphaVantageValidator(data).validate()
        return data

    async def stock_monthly_adjusted(self):
        data = await self._fetch_data('TIME_SERIES_MONTHLY_ADJUSTED')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('Monthly Adjusted Time Series', {}))

    async def stock_latest(self):
        data = await self._fetch_data('GLOBAL_QUOTE')
        await AlphaVantageValidator(data).validate()
        return data

    async def news(self):
        data = await self._fetch_data(f'NEWS_SENTIMENT&tickers={self.symbol}')
        await AlphaVantageValidator(data).validate()
        return pd.DataFrame(data.get('feed'))
