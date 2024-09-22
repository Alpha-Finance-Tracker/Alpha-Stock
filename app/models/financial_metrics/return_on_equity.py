# good above 5-7%

# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import NoContent


class ReturnOnEquity(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance
    async def evaluate(self):

        try:
            net_income = self.yahoo_finance.income_statement.loc['Net Income Common Stockholders'].iloc[0]
        except Exception as e:
            return 'net_income data missing'

        try:
            stockholders_equity = self.yahoo_finance.balance_sheet.loc['Stockholders Equity'].iloc[0]
        except Exception as e:
            return 'stockholders_equity data missing'


        return (net_income / stockholders_equity) * 100
