import pandas as pd
from async_lru import alru_cache

from app.models.calculators.profitability_metrics.profit_margins.gross_profit_margin import GrossProfitMargin
from app.models.calculators.profitability_metrics.profit_margins.net_profit_margin import NetProfitMargin
from app.models.calculators.profitability_metrics.profit_margins.operating_profit_margin import OperatingProfitMargin
from app.models.calculators.profitability_metrics.return_ratios.nopat import Nopat
from app.models.calculators.profitability_metrics.return_ratios.return_on_invested_capital import \
    ReturnOnInvestedCapital
from app.models.calculators.risk_measurement.levarage_ratios.cash_to_debt_ratio import CashToDebtRatio
from app.models.calculators.risk_measurement.levarage_ratios.debt_to_equity_ratio import DebtToEquityRatio
from app.models.calculators.risk_measurement.levarage_ratios.interest_coverage_ratio import InterestCoverageRatio
from app.models.calculators.risk_measurement.liquidity_ratios.current_ratio import CurrentRatio
from app.models.calculators.risk_measurement.solvency_ratios.debt_to_ebitda_ratio import DebtToEbitdaRatio
from app.models.calculators.risk_measurement.solvency_ratios.tax_rate import TaxRate
from app.models.data_stream.alpha_vantage_data import AlphaVantage


class AVCompanyAnalysis:

    def __init__(self,symbol):
        self.alpha_vantage = AlphaVantage(symbol)
        self.balance_sheet= self.alpha_vantage.balance_sheet()
        self.income_statement=self.alpha_vantage.income_statement()
        self.merged_df=pd.merge(self.income_statement, self.balance_sheet)


    async def roa_service(self):
        self.merged_df['netIncome']=pd.to_numeric(self.merged_df['netIncome'],errors='coerce')
        self.merged_df['totalAssets'] = pd.to_numeric(self.merged_df['totalAssets'], errors='coerce')

        self.merged_df['ROE'] = round(( self.merged_df['netIncome'] /  self.merged_df['totalAssets']) * 100,2)
        return  {row['fiscalDateEnding']: row['ROE'] for _, row in  self.merged_df.iterrows()}


    async def roe_service(self):
        self.merged_df['netIncome'] = pd.to_numeric(self.merged_df['netIncome'], errors='coerce')
        self.merged_df['totalShareholderEquity'] = pd.to_numeric(self.merged_df['totalShareholderEquity'], errors='coerce')

        self.merged_df['ROA'] = round(( self.merged_df['netIncome'] /  self.merged_df['totalShareholderEquity']) * 100,2)

        return  {row['fiscalDateEnding']: row['ROA'] for _, row in  self.merged_df.iterrows()}

    async def roic_service(self):


        # operating income
        self.merged_df['operatingIncome'] = pd.to_numeric( self.merged_df['operatingIncome'], errors='coerce')

        # invested capital
        self.merged_df['totalAssets'] = pd.to_numeric( self.merged_df['totalAssets'], errors='coerce')
        self.merged_df['totalLiabilities'] = pd.to_numeric( self.merged_df['totalLiabilities'], errors='coerce')
        self.merged_df['investedCapital'] =  self.merged_df['totalAssets'] -  self.merged_df['totalLiabilities']


        #tax rate
        self.merged_df['incomeBeforeTax'] = pd.to_numeric( self.merged_df['incomeBeforeTax'], errors='coerce')
        self.merged_df['incomeTaxExpense'] = pd.to_numeric( self.merged_df['incomeTaxExpense'], errors='coerce')


        tax_rates_instance = TaxRate(income_before_tax= self.merged_df['incomeBeforeTax'],
                                 income_after_tax= self.merged_df['incomeTaxExpense'])


        tax_rates = await tax_rates_instance.calculate()

        # NOPAT
        nopat_instance =  Nopat(operating_incomes= self.merged_df['operatingIncome'],
                            tax_rates=tax_rates)

        nopat = await nopat_instance.calculate()


        #ROIC
        roics = await ReturnOnInvestedCapital(nopat,  self.merged_df['investedCapital']).calculate()

        return {year:roic for year,roic in zip( self.merged_df['fiscalDateEnding'],roics)}


    async def cash_to_debt_service(self):
        self.merged_df['cashAndCashEquivalentsAtCarryingValue']=(
            pd.to_numeric( self.merged_df['cashAndCashEquivalentsAtCarryingValue'],errors='coerce'))

        self.merged_df['currentDebt'] = pd.to_numeric( self.merged_df['currentDebt'], errors='coerce')
        self.merged_df['longTermDebt'] = pd.to_numeric( self.merged_df['longTermDebt'], errors='coerce')

        self.merged_df['totalDebt'] =  self.merged_df['currentDebt'] +  self.merged_df['longTermDebt']

        return await CashToDebtRatio(cash_and_cash_equivalents= self.merged_df['cashAndCashEquivalentsAtCarryingValue'],
                                     total_debt= self.merged_df['totalDebt']).calculate()

    async  def debt_to_equity_service(self):
        self.merged_df['totalCurrentLiabilities'] = pd.to_numeric( self.merged_df['totalCurrentLiabilities'],errors='coerce')
        self.merged_df['totalShareholderEquity'] = pd.to_numeric( self.merged_df['totalShareholderEquity'],errors='coerce')

        return await DebtToEquityRatio(current_liabilities= self.merged_df['totalCurrentLiabilities'],
                                       stockholders_equity= self.merged_df['totalShareholderEquity']).calculate()

    async def interest_coverage_ratio_service(self):
        self.merged_df['ebit'] = pd.to_numeric(self.merged_df['ebit'], errors='coerce')
        self.merged_df['interestExpense'] = pd.to_numeric(self.merged_df['interestExpense'], errors='coerce')

        return await InterestCoverageRatio(ebit=self.merged_df['ebit'],
                                           interest_expense=self.merged_df['interestExpense']).calculate()

    async def current_ratio_service(self):
        self.merged_df['totalCurrentAssets'] = pd.to_numeric(self.merged_df['totalCurrentAssets'], errors='coerce')
        self.merged_df['totalCurrentLiabilities'] = pd.to_numeric(self.merged_df['totalCurrentLiabilities'], errors='coerce')

        return await CurrentRatio(current_assets=self.merged_df['totalCurrentAssets'],
                                  current_liabilities=self.merged_df['totalCurrentLiabilities']).calculate()


    async def debt_to_ebitda_service(self):
        self.merged_df['ebitda'] = pd.to_numeric(self.merged_df['ebitda'], errors='coerce')
        self.merged_df['totalCurrentLiabilities'] = pd.to_numeric(self.merged_df['totalCurrentLiabilities'],
                                                                  errors='coerce')
        self.merged_df['currentDebt'] = pd.to_numeric(self.merged_df['currentDebt'], errors='coerce')
        self.merged_df['longTermDebt'] = pd.to_numeric(self.merged_df['longTermDebt'], errors='coerce')

        self.merged_df['totalDebt'] = self.merged_df['currentDebt'] + self.merged_df['longTermDebt']

        return await DebtToEbitdaRatio(ebitda=self.merged_df['ebitda'],
                                       total_debt=self.merged_df['totalDebt']).calculate()

    async def gross_profit_margin(self):
        self.merged_df['grossProfit'] = pd.to_numeric(self.merged_df['grossProfit'], errors='coerce')
        self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')

        return await GrossProfitMargin(gross_profits=self.merged_df['grossProfit'],
                                       total_revenues=self.merged_df['totalRevenue']).calculate()

    async def net_profit_margin(self):
        self.merged_df['netIncome'] = pd.to_numeric(self.merged_df['netIncome'], errors='coerce')
        self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')

        return await NetProfitMargin(net_incomes=self.merged_df['netIncome'],
                                     total_revenues=self.merged_df['totalRevenue']).calculate()

    async def operating_profit_margin(self):
        self.merged_df['operatingIncome'] = pd.to_numeric(self.merged_df['operatingIncome'], errors='coerce')
        self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')

        return await OperatingProfitMargin(operating_incomes=self.merged_df['operatingIncome'],
                                           total_revenues=self.merged_df['totalRevenue']).calculate()

@alru_cache
async def cached_AVCompanyAnalysis(symbol: str):
    return AVCompanyAnalysis(symbol)
