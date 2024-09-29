import pandas as pd
from async_lru import alru_cache

from app.models.calculators.profitability_metrics.return_ratios.nopat import Nopat
from app.models.calculators.profitability_metrics.return_ratios.return_on_invested_capital import \
    ReturnOnInvestedCapital
from app.models.calculators.risk_measurement.solvency_ratios.tax_rate import TaxRate
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

        # operating income
        merged_df['operatingIncome'] = pd.to_numeric(merged_df['operatingIncome'], errors='coerce')

        # invested capital
        merged_df['totalAssets'] = pd.to_numeric(merged_df['totalAssets'], errors='coerce')
        merged_df['totalLiabilities'] = pd.to_numeric(merged_df['totalLiabilities'], errors='coerce')
        merged_df['investedCapital'] = merged_df['totalAssets'] - merged_df['totalLiabilities']


        #tax rate
        merged_df['incomeBeforeTax'] = pd.to_numeric(merged_df['incomeBeforeTax'], errors='coerce')
        merged_df['incomeTaxExpense'] = pd.to_numeric(merged_df['incomeTaxExpense'], errors='coerce')


        tax_rates = await TaxRate(income_before_tax=merged_df['incomeBeforeTax'],
                                 income_after_tax=merged_df['incomeTaxExpense']).calculate()

        # NOPAT
        nopat = await Nopat(operating_incomes=merged_df['operatingIncome'],
                            tax_rates=tax_rates).calculate()
        #ROIC
        roics = await ReturnOnInvestedCapital(nopat, merged_df['investedCapital']).calculate()

        return {year:roic for year,roic in zip(merged_df['fiscalDateEnding'],roics)}





@alru_cache
async def cached_AVCompanyAnalysis(symbol: str):
    return AVCompanyAnalysis(symbol)
