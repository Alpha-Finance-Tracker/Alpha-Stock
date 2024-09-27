import pandas as pd

from app.models.data_stream.alpha_vantage_data import AlphaVantage


class AVCompanyAnalysis:

    def __init__(self,symbol):
        self.alpha_vantage = AlphaVantage(symbol)

    async def roa_service(self):
        balance_sheet = await self.alpha_vantage.balance_sheet()
        income_statement = await self.alpha_vantage.income_statement()

        merged_df = pd.merge(income_statement, balance_sheet)

        merged_df['netIncome'] = pd.to_numeric(merged_df['netIncome'], errors='coerce')
        merged_df['totalAssets'] = pd.to_numeric(merged_df['totalAssets'], errors='coerce')


        merged_df['ROE'] = (merged_df['netIncome'] / merged_df['totalAssets']) * 100
        return  {row['fiscalDateEnding']: row['ROE'] for _, row in merged_df.iterrows()}


    async def roe_service(self):
        balance_sheet = await self.alpha_vantage.balance_sheet()
        income_statement = await self.alpha_vantage.income_statement()

        net_income = income_statement.loc['netIncome']
        stockholders_equity = balance_sheet.loc['totalShareholderEquity']

        net_income = net_income[net_income != 0]
        stockholders_equity = stockholders_equity[stockholders_equity != 0]

        roe = round((net_income / stockholders_equity) * 100, 2)
        return roe