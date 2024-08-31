from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance

class IntrinsicCalculatorUtilities:
    def __init__(self,data):
        self.data = data

    @property
    async def discount_rate(self):
        try:
            return await DiscountRate(self.data['income_statement'],
                                self.data['balance_sheet'],
                                self.data['company_overview'],
                                self.data['market_data'],
                                self.data['stock_info']).calculate()

        except Exception as e:
            raise e

    @property
    async def discounted_cash_flow(self):
        try:
            return await DiscountedCashFlow(self.data['cash_flows'],
                                      self.discount_rate).calculate()

        except Exception as e :
            raise e

    @property
    async def intrinsic_value(self):
        try:
            shares_outstanding = self.data['company_overview']['SharesOutstanding']
            return await IntrinsicValue(self.discounted_cash_flow,shares_outstanding).calculate()

        except Exception as e:
            raise e

    @property
    async def relative_value(self):
        try:
            return await RelativeValue(self.data['competitors_pe_ratio']).calculate()

        except Exception as e :
            raise e
