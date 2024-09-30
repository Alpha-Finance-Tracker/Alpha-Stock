import logging

from app.models.base_models.stock_calculator import StockCalculator
from app.models.data_stream.open_ai_data import OpenAIData
from app.utilities.responses import CalculationError


class RelativeValue(StockCalculator):

    def __init__(self, yahoo_finance):
        self.yahoo_finance = yahoo_finance

    async def calculate(self):
        try:
            competitors_price_to_earnings_ratio_list = await self.competitors()
            result = (sum(competitors_price_to_earnings_ratio_list) /
                      len(competitors_price_to_earnings_ratio_list))
            return round(result, 2)

        except (ZeroDivisionError, ValueError, TypeError, IndexError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()

    async def competitors(self):
        try:
            sector = self.yahoo_finance.info['sector']
            symbol = self.yahoo_finance.symbol
            return await OpenAIData(symbol).competitors_price_to_earnings_ratio(sector)
        except Exception as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()
