# good above 5-7%

# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class ReturnOnEquityYF(BasicMetricEvaluator):

    def __init__(self, yahoo_finance):
        self.yahoo_finance = yahoo_finance

    @property
    def roe(self):
        try:
            return self.yahoo_finance.info['returnOnEquity']
        except Exception as e:
            print(e)
            return NoContent(content='No Information found for roe for this company')

    async def evaluate(self):
        return self.roe

