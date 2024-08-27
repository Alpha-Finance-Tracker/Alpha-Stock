from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

from app.data.requests.stock_fetches import fetch_company_income_statement_av, fetch_company_balance_sheet_av, \
    fetch_company_annual_eps_av, fetch_company_cash_flows_av
from app.api.stock_and_company_features.stock_and_company_queries import send_parameters_towards_the_database
from app.data.database import read_query
from app.models.alpha_stock import AlphaStock
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.statements_and_reports.cash_flows import CashFlow
from app.models.statements_and_reports.debt import Debt
from app.models.statements_and_reports.earnings_per_share import EarningsPerShare

from app.models.statements_and_reports.net_income import NetIncome
from app.models.statements_and_reports.net_profit_margin import NetProfitMargin
from app.models.statements_and_reports.return_on_equity import ReturnOnEquity
from app.models.statements_and_reports.revenue_growth import RevenueGrowth
from app.utilities.service_utilities import display_charts

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


async def financial_performance(symbol):
    alpha_vantage = AlphaVantage()
    income_statement = alpha_vantage.fetch_company_income_statement(symbol)
    balance_sheet = alpha_vantage.fetch_company_balance_sheet(symbol)
    annual_eps = alpha_vantage.fetch_company_annual_eps(symbol)
    cash_flows = alpha_vantage.fetch_company_cash_flows(symbol)




    revenue_growth = RevenueGrowth(balance_sheet, income_statement).info()
    net_income = NetIncome(income_statement).info()
    earnings_per_share = EarningsPerShare(annual_eps).info()
    return_on_equity = ReturnOnEquity(balance_sheet, income_statement).info()
    net_profit_margin = NetProfitMargin(income_statement).info()
    debt_level = Debt(balance_sheet).info()
    cash_flow = CashFlow(cash_flows).info()

    await send_parameters_towards_the_database(revenue_growth,
                                               net_income,
                                               earnings_per_share,
                                               return_on_equity,
                                               net_profit_margin,
                                               debt_level,
                                               cash_flow,
                                               symbol)
    return 'Parameters successfully fetched and registered'


def fetch_company_info_from_db(symbol):
    data = read_query('SELECT * FROM company WHERE symbol = %s', (symbol,))
    img = display_charts(data)
    return img
