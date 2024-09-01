import asyncio
import time

from app.models.base_models.data_stream import DataStream


class IntrinsicValueDS(DataStream):

    def __init__(self,yahoo_finance,alpha_vantage,open_ai):
        self.yahoo_finance = yahoo_finance
        self.alpha_vantage = alpha_vantage
        self.open_ai = open_ai
        self.data = {}


        self.competitors_pe_ratio = None
        self.company_overview = None
        self.income_statement = None
        self.balance_sheet = None
        self.market_data = None
        self.cash_flow = None
        self.stock_info = None

    async def load(self):
        try:
            start_time = time.time()


            cash_flow = self.yahoo_finance.cash_flow
            stock_info = self.yahoo_finance.info
            company_overview = await self.alpha_vantage.company_overview()

            competitors_pe_ratio,income_statement, balance_sheet,market_data = await asyncio.gather(
                self.open_ai.competitors_price_to_earnings_ratio(company_overview['Sector']),
                self.alpha_vantage.income_statement(),
                self.alpha_vantage.balance_sheet(),
                self.yahoo_finance.market_data(),
                return_exceptions=True
            )


            self.data['company_overview'] = company_overview
            self.data['competitors_pe_ratio'] = competitors_pe_ratio
            self.data['income_statement'] = income_statement
            self.data['balance_sheet'] = balance_sheet
            self.data['market_data'] = market_data
            self.data['cash_flow'] = cash_flow
            self.data['stock_info'] = stock_info

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

        end_time = time.time()
        duration = end_time - start_time
        print(f"Asynchronous load took {duration} seconds")

    async def unload(self):
        try:
            await self.load()
            return self.data

        except Exception as e:
            raise  e