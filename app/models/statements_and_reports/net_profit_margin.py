from app.models.base_models.financial_statement import FinancialStatement
import pandas as pd


class NetProfitMargin(FinancialStatement):

    def __init__(self, income_statement):
        self.income_statement = income_statement
        self.updated = False

    def update(self):
        try:
            self.income_statement['netProfitMargin'] = (pd.to_numeric(self.income_statement['netIncome'],
                                                                      errors='coerce') / pd.to_numeric(
                self.income_statement['totalRevenue'], errors='coerce')) * 100

            self.income_statement['netProfitMargin'] = self.income_statement['netProfitMargin'].pct_change() * 100
            self.updated = True
        except Exception as e:
            print(f"Error with net_profit_margin {e}")
            return None

    def info(self):
        try:
            if not self.updated:
                self.update()
            return self.income_statement[['netProfitMargin', 'fiscalDateEnding']]
        except Exception as e:
            print(f"Error with net_profit_margin {e}")
            return None
