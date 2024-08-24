from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

from app.data.requests.stock_fetches import fetch_company_income_statement_av, fetch_company_balance_sheet_av, \
    fetch_company_annual_eps_av, fetch_company_cash_flows_av
from app.api.stock_and_company_features.stock_and_company_queries import send_parameters_towards_the_database
from app.data.database import read_query
from app.models.alpha_stock import AlphaStock
from app.utilities.service_utilities import display_charts
env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


async def financial_performance(symbol):
    income_statement = fetch_company_income_statement_av(symbol)  # fetch  income statement
    balance_sheet = fetch_company_balance_sheet_av(symbol)  # fetch balance sheet
    annual_eps = fetch_company_annual_eps_av(symbol)  # fetch annual eps
    cash_flows = fetch_company_cash_flows_av(symbol)  # fetch cash flow

    AS = AlphaStock(symbol=symbol, income_statement=income_statement, balance_sheet=balance_sheet,
                    annual_eps=annual_eps, cash_flows=cash_flows)

    revenue_for_14_years = AS.revenue
    net_income_for_14_years = AS.net_income
    eps_for_14_years = AS.eps
    roe_for_14_years = AS.roe
    net_profit_margin_for_14_years = AS.net_profit_margin
    debt_level_for_14_years = AS.debt
    cash_flows_for_14_years = AS.cash

    await send_parameters_towards_the_database(revenue_for_14_years,
                                               net_income_for_14_years,
                                               eps_for_14_years,
                                               roe_for_14_years,
                                               net_profit_margin_for_14_years,
                                               debt_level_for_14_years,
                                               cash_flows_for_14_years,
                                               symbol)
    return 'Parameters successfully fetched and registered'


def fetch_company_info_from_db(symbol):
    data =  read_query('SELECT * FROM company WHERE symbol = %s', (symbol,))
    img = display_charts(data)
    return img
