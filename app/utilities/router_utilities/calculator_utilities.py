from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance



async def intrinsic_value_calculator_service(symbol):
    services = await intrinsic_value_fetchers(symbol)
    data = await fetch_intrinsic_value_data(services)
    values = await intrinsic_value_necessary_calculations(data)

    return values


async def intrinsic_value_fetchers(symbol):

    return {'yahoo_finance':YahooFinance(symbol),
            'alpha_vantage':AlphaVantage(symbol),
            'open_ai':OpenAIData(symbol)}


async def fetch_intrinsic_value_data(services):
    yahoo_finance = services['yahoo_finance']
    alpha_vantage = services['alpha_vantage']
    open_ai = services['open_ai']

    try:
        market_data = yahoo_finance.market_data
        cash_flows = yahoo_finance.cash_flow
        stock_info = yahoo_finance.info

        company_overview =  alpha_vantage.company_overview()
        income_statement =  alpha_vantage.income_statement()
        balance_sheet =  alpha_vantage.balance_sheet()

        competitors_pe_ratio = open_ai.competitors_price_to_earnings_ratio(company_overview['Sector'])

    except Exception as e:
        # Handle or log the error
        raise e

    return {
        'market_data': market_data,
        'cash_flows': cash_flows,
        'stock_info': stock_info,
        'company_overview': company_overview,
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'competitors_pe_ratio': competitors_pe_ratio
    }


async def intrinsic_value_necessary_calculations(data):
    discount_rate = DiscountRate(
        data['income_statement'],
        data['balance_sheet'],
        data['company_overview'],
        data['market_data'],
        data['stock_info']
    ).calculate()

    discounted_cash_flow = DiscountedCashFlow(data['cash_flows'], discount_rate).calculate()
    intrinsic_value = IntrinsicValue(discounted_cash_flow, data['company_overview']['SharesOutstanding']).calculate()
    relative_value = RelativeValue(data['competitors_pe_ratio']).calculate()

    return {
        'Intrinsic_value': intrinsic_value,
        'Relative_value': relative_value
    }
