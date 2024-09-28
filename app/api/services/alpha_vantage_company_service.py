import pandas as pd
from async_lru import alru_cache

from app.models.data_stream.alpha_vantage_data import AlphaVantage


class AVCompanyAnalysis:

    def __init__(self,symbol):
        self.alpha_vantage = AlphaVantage(symbol)
        self.balance_sheet= self.alpha_vantage.balance_sheet()
        self.income_statement=self.alpha_vantage.income_statement()


    async def roa_service(self):
        merged_df = pd.merge(self.income_statement, self.balance_sheet)
        merged_df = merged_df.apply(pd.to_numeric, errors='coerce')


        merged_df['ROE'] = round((merged_df['netIncome'] / merged_df['totalAssets']) * 100,2)
        return  {row['fiscalDateEnding']: row['ROE'] for _, row in merged_df.iterrows()}


    async def roe_service(self):
        merged_df = pd.merge(self.income_statement, self.balance_sheet)
        merged_df = merged_df.apply(pd.to_numeric, errors='coerce')



        merged_df['ROA'] = round((merged_df['netIncome'] / merged_df['totalShareholderEquity']) * 100,2)

        return  {row['fiscalDateEnding']: row['ROA'] for _, row in merged_df.iterrows()}

    async def roic_service(self):
        merged_df = pd.merge(self.income_statement, self.balance_sheet)

        merged_df = merged_df.apply(pd.to_numeric, errors='coerce')



        merged_df['investedCapital'] = merged_df['totalAssets'] - merged_df['totalLiabilities']





@alru_cache
async def cached_AVCompanyAnalysis(symbol: str):
    return AVCompanyAnalysis(symbol)
