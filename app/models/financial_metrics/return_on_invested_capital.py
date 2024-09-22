# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.utilities.responses import CalculationError


class ReturnOnInvestedCapital(BasicMetricEvaluator):

    def __init__(self,yahoo_finance):
        self.yahoo_finance=yahoo_finance


    @property
    def nopat(self):
        operating_income = None
        tax_rate = 0.481

        try:
            operating_income_q1 = self.yahoo_finance.quarterly_income_statement.loc['Operating Income'].iloc[0]
            operating_income_q2 = self.yahoo_finance.quarterly_income_statement.loc['Operating Income'].iloc[1]
            operating_income_q3 = self.yahoo_finance.quarterly_income_statement.loc['Operating Income'].iloc[2]
            operating_income_q4 = self.yahoo_finance.quarterly_income_statement.loc['Operating Income'].iloc[3]
            operating_income = operating_income_q4 + operating_income_q3 + operating_income_q2 + operating_income_q1
            # tax_rate = self.yahoo_finance.income_statement.loc['Tax Rate For Calcs'].iloc[0]
        except Exception as e:
            pass
        print(operating_income)
        return operating_income * (1*tax_rate)


    @property
    def average_invested_capital(self):
        current = self.yahoo_finance.balance_sheet.loc['Invested Capital'].iloc[0]
        previous = self.yahoo_finance.balance_sheet.loc['Invested Capital'].iloc[1]

        return (current + previous) / 2
    async def evaluate(self):
        nopat = self.nopat
        avg_invested_capital = self.average_invested_capital

        return (nopat/avg_invested_capital) * 100
