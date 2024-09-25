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
from app.models.calculators.valuation.fair_value_calculator import FairValue
from app.models.calculators.valuation.relative_value_calculator import RelativeValue
from app.models.data_stream.open_ai_data import OpenAIData
from app.models.data_stream.yahoo_finance_data import YahooFinance
import pandas as pd

from app.utilities.responses import CalculationError


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

        return await CashToDebtRatio(total_debt,cash_and_cash_equivalents).calculate()

    async def debt_to_equity_service(self):
        current_liabilities=self.yahoo_finance.balance_sheet.loc['Current Liabilities']
        stockholders_equity=self.yahoo_finance.balance_sheet.loc['Stockholders Equity']

        return await DebtToEquityRatio(current_liabilities,stockholders_equity).calculate()


    async def interest_coverage_ratio_service(self):
        ebit=self.yahoo_finance.income_statement.loc['EBIT']
        interest_expense=self.yahoo_finance.income_statement.loc['Interest Expense']

        return await InterestCoverageRatio(ebit,interest_expense).calculate()

    async def current_ratio_service(self):
        current_assets=self.yahoo_finance.balance_sheet.loc['Current Assets']
        current_liabilities=self.yahoo_finance.balance_sheet.loc['Current Liabilities']

        return await CurrentRatio(current_assets,current_liabilities).calculate()

    async def debt_to_ebitda_service(self):
        ebitda=self.yahoo_finance.income_statement.loc['EBITDA']
        total_debt=self.yahoo_finance.balance_sheet.loc['Total Debt']

        return await DebtToEbitdaRatio(ebitda,total_debt).calculate()


    async def gross_profit_margin(self):
        gross_profits = self.yahoo_finance.income_statement.loc['Gross Profit']
        total_revenues = self.yahoo_finance.income_statement.loc['Total Revenue']

        return await GrossProfitMargin(gross_profits,total_revenues).calculate()

    async def net_profit_margin(self):
        net_incomes = self.yahoo_finance.income_statement.loc['Net Income']
        total_revenues = self.yahoo_finance.income_statement.loc['Total Revenue']

        return await NetProfitMargin(net_incomes,total_revenues).calculate()

    async def operating_profit_margin(self):
        operating_incomes = self.yahoo_finance.income_statement.loc['Operating Income']
        total_revenues = self.yahoo_finance.income_statement.loc['Total Revenue']

        return await OperatingProfitMargin(operating_incomes,total_revenues).calculate()

    async def price_valuations(self):
        company = self.yahoo_finance.info

        data = {'P/E ratio ':company['forwardPE'],
                'P/B ratio ':company['priceToBook'],
                'PEG ratio ':company['trailingPegRatio'],
                'P/S ratio ':company['priceToSalesTrailing12Months']}

        return data

    async def dcf(self):
        pass

    async def fair_value(self):
        return await FairValue(self.yahoo_finance).calculate()

    async def relative_value(self):
        return await RelativeValue(self.yahoo_finance).calculate()
