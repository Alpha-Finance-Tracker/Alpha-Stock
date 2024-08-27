import pandas as pd
import requests
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)




class AlphaVantage:
    def __init__(self):
        self.api_key = Alpha_vintage_key

    def fetch_company_balance_sheet(self,symbol):
        balance_sheet, _ = fd.get_balance_sheet_annual(symbol)
        return pd.DataFrame(balance_sheet)

    def fetch_company_income_statement(self, symbol):
        income_statement, _ = fd.get_income_statement_annual(symbol)
        return pd.DataFrame(income_statement)

    def fetch_company_cash_flows(self, stock):
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        annual_reports = data.get('annualReports')
        return pd.DataFrame(annual_reports)

    def fetch_company_pe_ratio(self, stock):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        annual_earnings = data.get('annualEarnings', [])
        return pd.DataFrame(annual_earnings)

    def fetch_company_overview(self, stock):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        return r.json()

    def fetch_company_annual_eps(self,stock):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        i = data.get('annualEarnings', [])
        return pd.DataFrame(i)

    def fetch_stock_minutes(self,stock: str, minutes: int):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={minutes}min&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data

    def fetch_stock_days(self,stock: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        return data

    def fetch_stock_weeks(self,stock: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        return data

    def fetch_stock_months(self,stock: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        return data

    def fetch_stock_monthly_adjusted(self,stock: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        return data

    def fetch_stock_latest(self,stock: str):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        return data
