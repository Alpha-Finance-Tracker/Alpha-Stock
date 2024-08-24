import pandas as pd
import requests
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.api.AI_features.open_ai_services import fetch_competitors

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_SECOND_KEY')
fd = FundamentalData(Alpha_vintage_key)

def fetch_company_income_statement_av(symbol):
    income_statement, _ = fd.get_income_statement_annual(symbol)
    return pd.DataFrame(income_statement)

def fetch_company_balance_sheet_av(symbol):
    balance_sheet, _ = fd.get_balance_sheet_annual(symbol)
    return pd.DataFrame(balance_sheet)

def fetch_cash_flow_yf(symbol):
    ticker = yf.Ticker(symbol)
    cash_flow = ticker.cash_flow
    cash_flow = cash_flow.infer_objects(copy=False).fillna(0)
    return pd.DataFrame(cash_flow)


def fetch_company_annual_eps_av(stock):
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    i =  data.get('annualEarnings', [])
    return pd.DataFrame(i)


def fetch_company_cash_flows_av(stock):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    annual_reports = data.get('annualReports')
    return pd.DataFrame(annual_reports)


def fetch_company_pe_ratio_yf(symbol):
    try:
        stock = yf.Ticker(symbol)
        pe_ratio = stock.info['forwardPE']
        return float(pe_ratio)
    except Exception as e:
        print(e)


def fetch_stock_minutes_av(stock: str, min: int):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={min}min&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data


def fetch_stock_days_av(stock: str):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_stock_weeks_av(stock: str):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_stock_months_av(stock: str):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_stock_monthly_adjusted_av(stock: str):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_stock_latest_av(stock: str):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_company_overview_av(stock):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data


def fetch_company_beta_yf(stock):
    # Yahoo
    stock_data = yf.Ticker(stock)
    historical_data = stock_data.history(period="max")

    # Calculate beta
    beta = historical_data['Close'].pct_change().cov(historical_data['Close'].pct_change())

    return beta


def fetch_market_data_yf(stock):
    # , start = '2010-01-01', end = '2023-01-01'
    market_data = yf.download(f'{stock}')
    return market_data


def fetch_competitors_eps_yf(symbol, sector):
    competitors = fetch_competitors(symbol, sector)
    competitors_pe_ratio = []

    for x in competitors:
        eps = fetch_company_pe_ratio_yf(x)
        if eps:
            competitors_pe_ratio.append(eps)

    return competitors_pe_ratio


