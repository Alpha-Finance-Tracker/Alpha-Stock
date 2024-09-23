# good if below  1 or 0.5
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class DebtToEquityRatio(StockCalculator):


    def __init__(self,current_liabilities,stockholders_equity):
        self.current_liabilities=current_liabilities
        self.stockholders_equity=stockholders_equity

    async def calculate(self):
        return self.current_liabilities / self.stockholders_equity
