from app.models.base_models.financial_statement import FinancialStatement

import pandas as pd


class ReturnOnEquity(FinancialStatement):

    def __init__(self,balance_sheet,income_statement):
        self.balance_sheet= balance_sheet
        self.income_statement = income_statement
        self.updated = False


    def update(self):
        try:
            self.balance_sheet['shareholdersEquity'] = (
                    pd.to_numeric(self.balance_sheet['totalAssets'], errors='coerce') - pd.to_numeric(
                self.balance_sheet['totalLiabilities'], errors='coerce'))

            self.balance_sheet['roe'] = (
                    pd.to_numeric(self.income_statement['netIncome'], errors='coerce') - self.balance_sheet[
                'shareholdersEquity'])
            self.updated = True
        except Exception as e:
            print(f"Error with roe: {e}")
            return None

    def info(self):
        try:
            if not self.updated:
                self.update()
            return  self.balance_sheet[['fiscalDateEnding', 'roe']]

        except Exception as e:
            print(f"Error with roe: {e}")
            return None
