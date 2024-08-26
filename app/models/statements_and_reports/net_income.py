from app.models.base_models.financial_statement import FinancialStatement


class NetIncome(FinancialStatement):

    def __init__(self, income_statement):
        self.income_statement = income_statement
        self.updated = False

    def info(self):
        try:

            return self.income_statement[['fiscalDateEnding', 'netIncome']]

        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    def update(self):
        pass
