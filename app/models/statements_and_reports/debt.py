from app.models.base_models.financial_statement import FinancialStatement


class Debt(FinancialStatement):

    def __init__(self, balance_sheet):
        self.balance_sheet = balance_sheet
        self.updated = False

    def info(self):
        try:
            result = self.balance_sheet[['currentDebt', 'fiscalDateEnding']]
            self.balance_sheet['currentDebt'] = self.balance_sheet['currentDebt'].fillna(0)

            return result
        except Exception as e:
            print(f"Error calculating debt level: {e}")
            return None

    def update(self):
        pass
