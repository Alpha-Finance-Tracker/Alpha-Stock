from app.models.calculators.profitability_metrics.return_ratios.nopat import Nopat
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





        # operating_income = self.yahoo_finance.income_statement.loc['Operating Income']
        # invested_capital = self.yahoo_finance.balance_sheet.loc['Invested Capital']
        #
        tax_rates = await TaxRate(self.yahoo_finance.income_statement).calculate()
        print(tax_rates)
        nopat = await Nopat(self.yahoo_finance.income_statement).calculate(tax_rates)
        print(nopat)










