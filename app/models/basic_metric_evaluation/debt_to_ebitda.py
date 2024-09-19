# good below 2.5
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class DebtToEbitda(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance






    async def evaluate(self):
        try:
            ebitda = self.yahoo_finance.income_statement.loc['EBITDA'].iloc[0]
            total_debt = self.yahoo_finance.balance_sheet.loc['Total Debt'].iloc[0]

            return total_debt / ebitda
        except Exception as e:
            print(e)
            return CalculationError(content='ebitda or total_debt missing')


