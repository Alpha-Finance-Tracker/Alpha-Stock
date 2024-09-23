# good above 5 or 10
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class InterestCoverageRatio(StockCalculator):


    def __init__(self,ebit,interest_expense):
        self.ebit = ebit
        self.interest_expense=interest_expense

    async def calculate(self):
        return self.ebit / self.interest_expense
