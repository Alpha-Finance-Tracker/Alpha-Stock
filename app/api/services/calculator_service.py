from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.intrinsic_value_ds import IntrinsicValueDS
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.calculator_utilities import IntrinsicCalculatorUtilities



class IntrinsicValueService:

    def __init__(self,symbol):
        self.symbol = symbol
        self.intrinsic_value = None
        self.relative_value = None

    async def present(self):
        return {'intrinsic_value':self.intrinsic_value,
                'relative_value': self.relative_value}

    async def service(self):
        yahoo_finance = YahooFinance(self.symbol)
        alpha_vantage = AlphaVantage(self.symbol)
        open_ai = OpenAIData(self.symbol)

        try:
            data = await IntrinsicValueDS(yahoo_finance, alpha_vantage, open_ai).unload()
            utilities = IntrinsicCalculatorUtilities(data)

            self.intrinsic_value = await utilities.intrinsic_value
            self.relative_value = await utilities.intrinsic_value

            return self.present()

        except Exception as e:
            raise e




