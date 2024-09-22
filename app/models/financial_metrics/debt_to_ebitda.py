from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator


class DebtToEbitda(BasicMetricEvaluator):


    def __init__(self,yahoo_finance):
        self.yahoo_finance=yahoo_finance
    async def evaluate(self):

        try:
            ebitda = self.yahoo_finance.income_statement.loc['EBITDA'].iloc[0]
        except Exception as e:
            return 'ebitda data missing'

        try:
            total_debt = self.yahoo_finance.balance_sheet.loc['Total Debt'].iloc[0]
        except Exception as e:
            return 'total_debt data missing'


        return total_debt / ebitda
