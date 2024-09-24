from app.models.calculators.profitability_metrics.return_ratios.nopat import Nopat
from app.models.calculators.profitability_metrics.return_ratios.return_on_invested_capital import \
    ReturnOnInvestedCapital
from app.models.calculators.risk_measurement.levarage_ratios.cash_to_debt import CashToDebt
from app.models.calculators.risk_measurement.levarage_ratios.debt_to_equity_ratio import DebtToEquity
from app.models.calculators.risk_measurement.levarage_ratios.interest_coverage_ratio import InterestCoverage
from app.models.calculators.risk_measurement.solvency_ratios.tax_rate import TaxRate
from app.models.data_stream.yahoo_finance_data import YahooFinance
import pandas as pd

class YFCompanyAnalysis:

    def __init__(self,symbol):
        self.yahoo_finance = YahooFinance(symbol)


    async def roa_service(self):
        total_assets = self.yahoo_finance.balance_sheet.loc['Total Assets']
        net_income_common_stockholders = self.yahoo_finance.income_statement.loc['Net Income Common Stockholders']

        total_assets = total_assets[total_assets != 0]
        net_income_common_stockholders = net_income_common_stockholders[net_income_common_stockholders != 0]

        roa = round((net_income_common_stockholders / total_assets) * 100,2)
        return roa

    async def roe_service(self):
        net_income_common_stockholders = self.yahoo_finance.income_statement.loc['Net Income Common Stockholders']
        stockholders_equity  = self.yahoo_finance.balance_sheet.loc['Stockholders Equity']

        net_income_common_stockholders = net_income_common_stockholders[net_income_common_stockholders != 0]
        stockholders_equity = stockholders_equity[stockholders_equity !=0]

        roe = round((net_income_common_stockholders / stockholders_equity )*100,2)
        return roe

    async def roic_service(self):
        operating_incomes = self.yahoo_finance.income_statement.loc['Operating Income']
        invested_capital = self.yahoo_finance.balance_sheet.loc['Invested Capital']

        tax_rates = await TaxRate(self.yahoo_finance.income_statement).calculate()
        nopat = await Nopat(operating_incomes,tax_rates).calculate()
        roic = await ReturnOnInvestedCapital(nopat,invested_capital).calculate()
        return roic

    async def cash_to_debt_service(self):

        total_debt = self.yahoo_finance.balance_sheet.loc['Total Debt']
        cash_and_cash_equivalents = self.yahoo_finance.balance_sheet.loc['Cash And Cash Equivalents']

        return await CashToDebt(total_debt,cash_and_cash_equivalents).calculate()

    async def debt_to_equity_service(self):
        current_liabilities=self.yahoo_finance.balance_sheet.loc['Current Liabilities']
        stockholders_equity=self.yahoo_finance.balance_sheet.loc['Stockholders Equity']

        return await DebtToEquity(current_liabilities,stockholders_equity).calculate()


    async def interest_coverage_ratio_service(self):
        ebit=self.yahoo_finance.income_statement.loc['EBIT']
        interest_expense=self.yahoo_finance.income_statement.loc['Interest Expense']

        return await InterestCoverage(ebit,interest_expense).calculate()






