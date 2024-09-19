# good above 1
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class CurrentRatio(BasicMetricEvaluator):


    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance


    @property
    def latest_current_ratio(self):
        try:
            return self.yahoo_finance.info['currentRatio']
        except Exception as e:
            print(e)
            return NoContent(content='Current Ratio param missing')

    async def evaluate(self):
        return self.latest_current_ratio
