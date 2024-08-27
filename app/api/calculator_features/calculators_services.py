from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.yahoo_finance_data import YahooFinance


async def intrinsic_value_calculator(symbol):
    yahoo_finance = YahooFinance()
    alpha_vantage = AlphaVantage()


    market_data = yahoo_finance.fetch_market_data(symbol)
    cash_flows = yahoo_finance.fetch_cash_flow(symbol)
    company_overview = alpha_vantage.fetch_company_overview(symbol)
    income_statement = alpha_vantage.fetch_company_income_statement(symbol)
    balance_sheet = alpha_vantage.fetch_company_balance_sheet(symbol)
    competitors_pe_ratio = yahoo_finance.fetch_competitors_eps(symbol,company_overview['Sector'])


    discount_rate = DiscountRate(income_statement,balance_sheet,company_overview,market_data).calculate()
    discounted_cash_flow = DiscountedCashFlow(cash_flows,discount_rate).calculate()
    intrinsic_value = IntrinsicValue(discounted_cash_flow,company_overview['SharesOutstanding']).calculate()
    relative_value = RelativeValue(competitors_pe_ratio).calculate()

    return (intrinsic_value+relative_value) / 2








#
# async def intrinsic_value_calculator(symbol):
#     market_data = fetch_market_data_yf(symbol)
#     cash_flows = fetch_cash_flow_yf(symbol)
#     co = fetch_company_overview_av(symbol)
#     income_statement = fetch_company_income_statement_av(symbol)
#     balance_sheet = fetch_company_balance_sheet_av(symbol)
#     competitors_pe_ratio = fetch_competitors_eps_yf(symbol,co['Sector'])
#
#     try:
#         AS = AlphaStock(symbol=symbol,
#                         cash_flows=cash_flows, co=co, market_data=market_data,
#                         income_statement=income_statement, balance_sheet=balance_sheet,competitors_pe_ratio=competitors_pe_ratio)
#
#         company_overview_db_update(co, symbol)
#         dcf_ps = AS.calculate_intrinsic_value_per_share
#         relative_value = AS.calculate_relative_value_per_share
#
#         return (dcf_ps + relative_value) // 2
#
#
#     except Exception as e:
#         return (f"Error with {e}")
#
