# good above 5 or 10

from app.models.base_models.stock_calculator import StockCalculator


class InterestCoverageRatio(StockCalculator):

    def __init__(self, ebit, interest_expense):
        self.ebit = ebit
        self.interest_expense = interest_expense

    def __repr__(self):
        return (f"InterestCoverageRatio(ebit={self.ebit}, "
                f"interest_expense={self.interest_expense})")

    async def calculate(self):
        interest_coverage = self.ebit / self.interest_expense
        interest_coverage = interest_coverage.round(2).dropna()
        return interest_coverage
