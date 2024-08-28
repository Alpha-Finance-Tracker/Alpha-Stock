from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance
async def intrinsic_value_calculator_service(symbol):
    # Data Fetchers
    yahoo_finance = YahooFinance(symbol)
    alpha_vantage = AlphaVantage(symbol)
    open_ai = OpenAIData()

    # Yahoo Data
    market_data = yahoo_finance.market_data(symbol)
    cash_flows = yahoo_finance.cash_flow(symbol)
    stock_info = yahoo_finance.info

    # Alpha Vantage Data
    company_overview = alpha_vantage.company_overview()
    income_statement = alpha_vantage.income_statement()
    balance_sheet = alpha_vantage.balance_sheet()

    # OpenAI data
    competitors_list = open_ai.fetch_competitors(symbol, company_overview['Sector'])
    competitors_price_to_earnings_ratio = [YahooFinance(company).info['forwardPe'] for company in competitors_list]

    # Calculators
    discount_rate = DiscountRate(income_statement, balance_sheet, company_overview, market_data,stock_info).calculate()
    discounted_cash_flow = DiscountedCashFlow(cash_flows, discount_rate).calculate()
    intrinsic_value = IntrinsicValue(discounted_cash_flow, company_overview['SharesOutstanding']).calculate()
    relative_value = RelativeValue(competitors_price_to_earnings_ratio).calculate()

    return (intrinsic_value + relative_value) / 2
