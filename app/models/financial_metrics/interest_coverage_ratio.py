# good above 5 or 10
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class InterestCoverageRatio(BasicMetricEvaluator):


    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance

    async def evaluate(self):

        try:
            ebit = self.yahoo_finance.income_statement.loc['EBIT'].iloc[0]
        except Exception as e:
            return 'EBIT data missing'

        try:
            interest_expense = self.yahoo_finance.income_statement.loc['Interest Expense'].iloc[0]
        except Exception as e:
            return 'interest_expense data missing'

        return ebit / interest_expense
