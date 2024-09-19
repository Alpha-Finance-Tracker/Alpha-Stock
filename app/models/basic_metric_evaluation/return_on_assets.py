# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class ReturnOnAssets(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance


    @property
    def roa(self):
        try:
            return self.yahoo_finance.info['returnOnAssets']
        except Exception as e:
            print(e)
            return NoContent(content='No Information found for roa for this company')

    async def evaluate(self):
        return self.roa


