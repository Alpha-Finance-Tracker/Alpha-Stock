from app.models.base_models.financial_statement import FinancialStatement

class CashFlow(FinancialStatement):

    def __init__(self, cash_flows):
        self.cash_flows = cash_flows
        self.updated = False

    def update(self):
        pass

    def info(self):
        try:
            return self.cash_flows[['fiscalDateEnding', 'operatingCashflow']]
        except Exception as e:
            print(f"Error with cash method: {e}")
            return None
