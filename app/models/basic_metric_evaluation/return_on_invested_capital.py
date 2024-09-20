# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class ReturnOnInvestedCapital(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance = yahoo_finance

    async def evaluate(self):
        try:

            net_profit = self.yahoo_finance.income_statement.loc['Net Income'].iloc[0]
            invested_capital = self.yahoo_finance.balance_sheet.loc['Invested Capital'].iloc[0]
            dividends = self.yahoo_finance.info['trailingAnnualDividendRate']
            return (net_profit - dividends) / invested_capital
        except Exception as e:
            print(e)
            return CalculationError(content='Error calculating roic, missing dividends ot net_profit or invested_capital')
