from app.models.base_models.financial_statement import FinancialStatement


class EarningsPerShare(FinancialStatement):

    def __init__(self, annual_earnings_per_share):
        self.annual_earnings_per_share = annual_earnings_per_share
        self.updated = False

    def info(self):
        try:
            return self.annual_earnings_per_share[['fiscalDateEnding', 'reportedEPS']]
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    def update(self):
        pass
