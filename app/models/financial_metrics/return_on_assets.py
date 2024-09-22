# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class ReturnOnAssets(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance

    async def evaluate(self):

        try:
            net_income = self.yahoo_finance.income_statement.loc['Net Income Continuous Operations'].iloc[0]
        except Exception as e:
            return 'net_income data missing'

        try:
            total_assets = self.yahoo_finance.balance_sheet.loc['Total Assets'].iloc[0]
        except Exception as e:
            return 'total_assets data missing'

        return (net_income/total_assets)*100

