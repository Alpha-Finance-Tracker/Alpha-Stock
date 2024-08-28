from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance
async def intrinsic_value_calculator_service(symbol):
    # Data Fetchers
    yahoo_finance = YahooFinance()
    alpha_vantage = AlphaVantage()
    open_ai = OpenAIData()

    # Yahoo Data
    market_data = yahoo_finance.fetch_market_data(symbol)
    cash_flows = yahoo_finance.fetch_cash_flow(symbol)

    # Alpha Vantage Data
    company_overview = alpha_vantage.company_overview(symbol)
    income_statement = alpha_vantage.income_statement(symbol)
    balance_sheet = alpha_vantage.balance_sheet(symbol)

    # OpenAI data
    competitors_list = open_ai.fetch_competitors(symbol, company_overview['Sector'])
    competitors_price_to_earnings_ratio = [
        yahoo_finance.fetch_company_price_to_earnings_ratio(company) for company in competitors_list]

    # Calculators
    discount_rate = DiscountRate(income_statement, balance_sheet, company_overview, market_data).calculate()
    discounted_cash_flow = DiscountedCashFlow(cash_flows, discount_rate).calculate()
    intrinsic_value = IntrinsicValue(discounted_cash_flow, company_overview['SharesOutstanding']).calculate()
    relative_value = RelativeValue(competitors_price_to_earnings_ratio).calculate()

    return (intrinsic_value + relative_value) / 2
