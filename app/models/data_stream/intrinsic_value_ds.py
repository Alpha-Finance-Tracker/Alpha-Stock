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
            company_overview = await self.alpha_vantage.company_overview()
            competitors_pe_ratio = await self.open_ai.competitors_price_to_earnings_ratio(company_overview['Sector'])

            self.data['company_overview'] =company_overview
            self.data['competitors_pe_ratio'] = competitors_pe_ratio
            self.data['income_statement'] = await self.alpha_vantage.income_statement()
            self.data['balance_sheet'] = await self.alpha_vantage.balance_sheet()
            self.data['market_data'] =  self.yahoo_finance.market_data
            self.data['cash_flow'] =  self.yahoo_finance.cash_flow
            self.data['stock_info'] =  self.yahoo_finance.info

        except Exception as e:
            raise  e

        end_time = time.time()
        duration = end_time - start_time
        print(f"Synchronous load took {duration} seconds")

    # async def load(self):
    #     try:
    #         start_time = time.time()
    #
    #         # Start all fetch operations concurrently
    #         company_overview_task = self.company_overview()
    #         income_statement_task = self.alpha_vantage.income_statement()
    #         balance_sheet_task = self.alpha_vantage.balance_sheet()
    #         market_data_task = self.yahoo_finance.market_data
    #         cash_flow_task = self.yahoo_finance.cash_flow()
    #         stock_info_task = self.yahoo_finance.info()
    #
    #         # Wait for the company overview to complete
    #         company_overview = await company_overview_task
    #
    #         # Start the competitors P/E ratio fetch after the company overview completes
    #         competitors_pe_ratio_task = self.open_ai.competitors_price_to_earnings_ratio(company_overview['Sector'])
    #
    #         # Wait for all other tasks to complete
    #         income_statement, balance_sheet, market_data, cash_flow, stock_info, competitors_pe_ratio = await asyncio.gather(
    #             income_statement_task,
    #             balance_sheet_task,
    #             market_data_task,
    #             cash_flow_task,
    #             stock_info_task,
    #             competitors_pe_ratio_task
    #         )
    #
    #         # Populate data dictionary with results
    #         self.data['company_overview'] = company_overview
    #         self.data['competitors_pe_ratio'] = competitors_pe_ratio
    #         self.data['income_statement'] = income_statement
    #         self.data['balance_sheet'] = balance_sheet
    #         self.data['market_data'] = market_data
    #         self.data['cash_flow'] = cash_flow
    #         self.data['stock_info'] = stock_info
    #
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return None
    #
    #     end_time = time.time()
    #     duration = end_time - start_time
    #     print(f"Asynchronous load took {duration} seconds")

    async def unload(self):
        try:
            await self.load()
            return self.data

        except Exception as e:
            raise  e