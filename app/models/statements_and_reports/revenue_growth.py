from app.models.base_models.financial_statement import FinancialStatement

import pandas as pd


class RevenueGrowth(FinancialStatement):

    def __init__(self, balance_sheet, income_statement):
        self.balance_sheet = balance_sheet
        self.income_statement = income_statement
        self.updated = False

    def update(self):
        try:
            self.income_statement['fiscalDateEnding'] = pd.to_datetime(self.income_statement['fiscalDateEnding'])
            self.income_statement['totalRevenue'] = pd.to_numeric(self.income_statement['totalRevenue'],
                                                                  errors='coerce')
            self.income_statement['growth_rate'] = self.income_statement[
                                                       'totalRevenue'].pct_change() * 100

            self.income_statement['growth_rate'] = self.income_statement['growth_rate'].fillna(0)
            self.updated = True
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    def info(self):
        try:
            if not self.updated:
                self.update()
            return self.income_statement[['growth_rate', 'fiscalDateEnding']]

        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None
