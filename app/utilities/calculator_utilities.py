from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance

class IntrinsicCalculatorUtilities:
    def __init__(self, symbol):
        self.symbol = symbol
        self.yahoo_finance = YahooFinance(symbol)
        self.alpha_vantage = AlphaVantage(symbol)
        self.open_ai = OpenAIData(symbol)
        self.valuation_data = self.data()


    @property
    async def present(self):
        return {'intrinsic_value':self.intrinsic_value,
                'relative_value':self.relative_value}


    def data(self):
        income_statement = self.alpha_vantage.income_statement()
        balance_sheet = self.alpha_vantage.balance_sheet()
        company_overview = self.alpha_vantage.company_overview()

        market_data = self.yahoo_finance.market_data
        cash_flows = self.yahoo_finance.cash_flow
        stock_info = self.yahoo_finance.info


        competitors_pe_ratio_data = self.open_ai.competitors_price_to_earnings_ratio(company_overview['Sector'])


        data = {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'company_overview': company_overview,
            'market_data': market_data,
            'cash_flows': cash_flows,
            'stock_info': stock_info,
            'competitors_pe_ratio': competitors_pe_ratio_data
        }

        return data


    @property
    def discount_rate(self):
        try:
            return DiscountRate(self.valuation_data['income_statement'],
                                self.valuation_data['balance_sheet'],
                                self.valuation_data['company_overview'],
                                self.valuation_data['market_data'],
                                self.valuation_data['stock_info']).calculate()

        except Exception as e:
            raise e

    @property
    def discounted_cash_flow(self):
        try:
            return DiscountedCashFlow(self.valuation_data['cash_flows'],
                                      self.discount_rate).calculate()

        except Exception as e :
            raise e

    @property
    def intrinsic_value(self):
        try:
            shares_outstanding = self.valuation_data['company_overview']['SharesOutstanding']
            return IntrinsicValue(self.discounted_cash_flow,shares_outstanding).calculate()

        except Exception as e:
            raise e

    @property
    def relative_value(self):
        try:
            return RelativeValue(self.valuation_data['competitors_pe_ratio']).calculate()

        except Exception as e :
            raise e
