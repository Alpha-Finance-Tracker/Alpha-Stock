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
from app.utilities.responses import CalculationError


class AVCompanyAnalysis:

    def __init__(self, symbol):
        try:
            self.alpha_vantage = AlphaVantage(symbol)
            self.balance_sheet = self.alpha_vantage.balance_sheet()
            self.income_statement = self.alpha_vantage.income_statement()
            self.merged_df = pd.merge(self.income_statement, self.balance_sheet)
        except Exception as e:
            raise CalculationError(f"Error initializing AVCompanyAnalysis: {str(e)}")

    async def roa_service(self):
        try:
            self.merged_df['netIncome'] = pd.to_numeric(self.merged_df['netIncome'], errors='coerce')
            self.merged_df['totalAssets'] = pd.to_numeric(self.merged_df['totalAssets'], errors='coerce')
            self.merged_df['ROA'] = round((self.merged_df['netIncome'] / self.merged_df['totalAssets']) * 100, 2)
            return {year: roe for year, roe in zip(self.merged_df['fiscalDateEnding'], self.merged_df['ROA'])}
        except Exception as e:
            raise CalculationError(f"Error in ROA service: {str(e)}")

    async def roe_service(self):
        try:
            self.merged_df['netIncome'] = pd.to_numeric(self.merged_df['netIncome'], errors='coerce')
            self.merged_df['totalShareholderEquity'] = pd.to_numeric(self.merged_df['totalShareholderEquity'],
                                                                     errors='coerce')
            self.merged_df['ROE'] = round(
                (self.merged_df['netIncome'] / self.merged_df['totalShareholderEquity']) * 100, 2)
            return {year: roe for year, roe in zip(self.merged_df['fiscalDateEnding'], self.merged_df['ROE'])}
        except Exception as e:
            raise CalculationError(f"Error in ROE service: {str(e)}")

    async def roic_service(self):
        try:
            self.merged_df['operatingIncome'] = pd.to_numeric(self.merged_df['operatingIncome'], errors='coerce')
            self.merged_df['totalAssets'] = pd.to_numeric(self.merged_df['totalAssets'], errors='coerce')
            self.merged_df['totalLiabilities'] = pd.to_numeric(self.merged_df['totalLiabilities'], errors='coerce')
            self.merged_df['investedCapital'] = self.merged_df['totalAssets'] - self.merged_df['totalLiabilities']
            self.merged_df['incomeBeforeTax'] = pd.to_numeric(self.merged_df['incomeBeforeTax'], errors='coerce')
            self.merged_df['incomeTaxExpense'] = pd.to_numeric(self.merged_df['incomeTaxExpense'], errors='coerce')

            tax_rates_instance = TaxRate(income_before_tax=self.merged_df['incomeBeforeTax'],
                                         income_after_tax=self.merged_df['incomeTaxExpense'])
            tax_rates = await tax_rates_instance.calculate()

            nopat_instance = Nopat(operating_incomes=self.merged_df['operatingIncome'], tax_rates=tax_rates)
            nopat = await nopat_instance.calculate()

            roics = await ReturnOnInvestedCapital(nopat, self.merged_df['investedCapital']).calculate()
            return {year: roic for year, roic in zip(self.merged_df['fiscalDateEnding'], roics)}

        except Exception as e:
            raise CalculationError(f"Error in ROIC service: {str(e)}")

    async def cash_to_debt_service(self):
        try:
            self.merged_df['cashAndCashEquivalentsAtCarryingValue'] = pd.to_numeric(
                self.merged_df['cashAndCashEquivalentsAtCarryingValue'], errors='coerce')
            self.merged_df['currentDebt'] = pd.to_numeric(self.merged_df['currentDebt'], errors='coerce')
            self.merged_df['longTermDebt'] = pd.to_numeric(self.merged_df['longTermDebt'], errors='coerce')
            self.merged_df['totalDebt'] = self.merged_df['currentDebt'] + self.merged_df['longTermDebt']
            cash_to_debt = await CashToDebtRatio(
                cash_and_cash_equivalents=self.merged_df['cashAndCashEquivalentsAtCarryingValue'],
                total_debt=self.merged_df['totalDebt']).calculate()

            return {year: cash for year, cash in zip(self.merged_df['fiscalDateEnding'], cash_to_debt)}
        except Exception as e:
            raise CalculationError(f"Error in Cash to Debt service: {str(e)}")

    async def debt_to_equity_service(self):
        try:
            self.merged_df['totalCurrentLiabilities'] = pd.to_numeric(self.merged_df['totalCurrentLiabilities'],
                                                                      errors='coerce')
            self.merged_df['totalShareholderEquity'] = pd.to_numeric(self.merged_df['totalShareholderEquity'],
                                                                     errors='coerce')
            debts = await DebtToEquityRatio(current_liabilities=self.merged_df['totalCurrentLiabilities'],
                                            stockholders_equity=self.merged_df['totalShareholderEquity']).calculate()

            return {year: debt for year, debt in zip(self.merged_df['fiscalDateEnding'], debts)}
        except Exception as e:
            raise CalculationError(f"Error in Debt to Equity service: {str(e)}")

    async def interest_coverage_ratio_service(self):
        try:
            self.merged_df['ebit'] = pd.to_numeric(self.merged_df['ebit'], errors='coerce')
            self.merged_df['interestExpense'] = pd.to_numeric(self.merged_df['interestExpense'], errors='coerce')
            interests = await InterestCoverageRatio(ebit=self.merged_df['ebit'],
                                                    interest_expense=self.merged_df['interestExpense']).calculate()

            return {year: interest for year, interest in zip(self.merged_df['fiscalDateEnding'], interests)}
        except Exception as e:
            raise CalculationError(f"Error in Interest Coverage Ratio service: {str(e)}")

    async def current_ratio_service(self):
        try:
            self.merged_df['totalCurrentAssets'] = pd.to_numeric(self.merged_df['totalCurrentAssets'], errors='coerce')
            self.merged_df['totalCurrentLiabilities'] = pd.to_numeric(self.merged_df['totalCurrentLiabilities'],
                                                                      errors='coerce')
            current_ratios = await CurrentRatio(current_assets=self.merged_df['totalCurrentAssets'],
                                                current_liabilities=self.merged_df[
                                                    'totalCurrentLiabilities']).calculate()

            return {year: current_ratio for year, current_ratio in
                    zip(self.merged_df['fiscalDateEnding'], current_ratios)}
        except Exception as e:
            raise CalculationError(f"Error in Current Ratio service: {str(e)}")

    async def debt_to_ebitda_service(self):
        try:
            self.merged_df['ebitda'] = pd.to_numeric(self.merged_df['ebitda'], errors='coerce')
            self.merged_df['totalCurrentLiabilities'] = pd.to_numeric(self.merged_df['totalCurrentLiabilities'],
                                                                      errors='coerce')
            self.merged_df['currentDebt'] = pd.to_numeric(self.merged_df['currentDebt'], errors='coerce')
            self.merged_df['longTermDebt'] = pd.to_numeric(self.merged_df['longTermDebt'], errors='coerce')
            self.merged_df['totalDebt'] = self.merged_df['currentDebt'] + self.merged_df['longTermDebt']
            debt_to_ebitdas = await DebtToEbitdaRatio(ebitda=self.merged_df['ebitda'],
                                                      total_debt=self.merged_df['totalDebt']).calculate()

            return {year: debt for year, debt in
                    zip(self.merged_df['fiscalDateEnding'], debt_to_ebitdas)}

        except Exception as e:
            raise CalculationError(f"Error in Debt to EBITDA service: {str(e)}")

    async def gross_profit_margin(self):
        try:
            self.merged_df['grossProfit'] = pd.to_numeric(self.merged_df['grossProfit'], errors='coerce')
            self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')
            gross_profits = await GrossProfitMargin(gross_profits=self.merged_df['grossProfit'],
                                                    total_revenues=self.merged_df['totalRevenue']).calculate()

            return {year: gross for year, gross in
                    zip(self.merged_df['fiscalDateEnding'], gross_profits)}
        except Exception as e:
            raise CalculationError(f"Error in Gross Profit Margin service: {str(e)}")

    async def net_profit_margin(self):
        try:
            self.merged_df['netIncome'] = pd.to_numeric(self.merged_df['netIncome'], errors='coerce')
            self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')
            net_profits = await NetProfitMargin(net_incomes=self.merged_df['netIncome'],
                                                total_revenues=self.merged_df['totalRevenue']).calculate()

            return {year: net for year, net in
                    zip(self.merged_df['fiscalDateEnding'], net_profits)}
        except Exception as e:
            raise CalculationError(f"Error in Net Profit Margin service: {str(e)}")

    async def operating_profit_margin(self):
        try:
            self.merged_df['operatingIncome'] = pd.to_numeric(self.merged_df['operatingIncome'], errors='coerce')
            self.merged_df['totalRevenue'] = pd.to_numeric(self.merged_df['totalRevenue'], errors='coerce')
            operating_profit_margins = await OperatingProfitMargin(operating_incomes=self.merged_df['operatingIncome'],
                                                                   total_revenues=self.merged_df[
                                                                       'totalRevenue']).calculate()

            return {year: operating_profit_margin for year, operating_profit_margin in
                    zip(self.merged_df['fiscalDateEnding'], operating_profit_margins)}
        except Exception as e:
            raise CalculationError(f"Error in Operating Profit Margin service: {str(e)}")

    async def news(self):
        try:
            data = self.alpha_vantage.news()


            times = [(x[0:4] + " " + x[4:6] + "." + x[6:8]) for x in data['time_published']]
            news = {'Title': data['title'],
                    'Url': data['url'],
                    'Time': times,
                    'Image': data['banner_image']}

            return news
        except Exception as e:
            return f'Error with parsing data from AV, probably fetch limit related {e}'


@alru_cache
async def cached_AVCompanyAnalysis(symbol: str):
    try:
        return AVCompanyAnalysis(symbol)
    except Exception as e:
        raise CalculationError(f"Error caching AVCompanyAnalysis: {str(e)}")
