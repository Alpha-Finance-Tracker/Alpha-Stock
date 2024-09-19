from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class Ebitda(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance

    @property
    def latest_ebitda(self):
        return self.yahoo_finance.income_statement.loc['EBITDA'].iloc[0]

    @property
    def historical_ebitda(self):
        return self.yahoo_finance.income_statement.loc['EBITDA']


    async def evaluate(self):

        try:
            return self.latest_ebitda
        except Exception as e:
            print(e)
            return CalculationError(content='Ebitda missing')



