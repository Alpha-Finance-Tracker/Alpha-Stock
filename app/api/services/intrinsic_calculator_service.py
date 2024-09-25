from app.models.base_models.service import Service
from app.models.calculators.discount_and_growth_rates.discount_rate_calculator import DiscountRate
from app.models.calculators.valuation.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.valuation.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.valuation.relative_value_calculator import RelativeValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.intrinsic_value_ds import IntrinsicValueDS
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance


class IntrinsicCalculatorService(Service):

    def __init__(self, symbol):
        self.symbol = symbol
        self.intrinsic_value = None
        self.relative_value = None

        self.yahoo_finance = YahooFinance(self.symbol)
        self.alpha_vantage = AlphaVantage(self.symbol)
        self.open_ai = OpenAIData(self.symbol)

    async def service(self):
        try:
            data = await IntrinsicValueDS(self.yahoo_finance, self.alpha_vantage, self.open_ai).unload()

            discount_rate = await DiscountRate(data['income_statement'], data['balance_sheet'],
                                               data['company_overview'],
                                               data['market_data'], data['stock_info']).calculate()

            discounted_cash_flow = await DiscountedCashFlow(data['cash_flow'], discount_rate).calculate()

            self.relative_value = await RelativeValue(data['competitors_pe_ratio']).calculate()
            self.intrinsic_value = await IntrinsicValue(discounted_cash_flow,
                                                        data['company_overview']['SharesOutstanding']).calculate()

            return await self.present()

        except Exception as e:
            raise e

    async def present(self):
        return {'intrinsic_value': self.intrinsic_value,
                'relative_value': self.relative_value,
                'average_value': self.intrinsic_value / self.relative_value}
