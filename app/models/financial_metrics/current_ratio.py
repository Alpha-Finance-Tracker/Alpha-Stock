# good above 1
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class CurrentRatio(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance
    async def evaluate(self):

        try:
            current_assets = self.yahoo_finance.balance_sheet.loc['Current Assets'].iloc[0]
        except Exception as e:
            return 'current_assets data missing'

        try:
            current_liabilities = self.yahoo_finance.balance_sheet.loc['Current Liabilities'].iloc[0]
        except Exception as e:
            return 'current_liabilities data missing'

        return current_assets / current_liabilities
