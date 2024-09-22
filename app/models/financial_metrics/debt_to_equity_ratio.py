# good if below  1 or 0.5
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class DebtToEquityRatio(BasicMetricEvaluator):


    def __init__(self,yahoo_finance):
        self.yahoo_finance=yahoo_finance

    async def evaluate(self):

        try:
            current_liabilities = self.yahoo_finance.balance_sheet.loc['Current Liabilities'].iloc[0]
        except Exception as e:
            return 'current_liabilities data missing'

        try:
            stockholders_equity = self.yahoo_finance.balance_sheet.loc['Stockholders Equity'].iloc[0]
        except Exception as e:
            return 'stockholders_equity data missing'

        return current_liabilities / stockholders_equity
