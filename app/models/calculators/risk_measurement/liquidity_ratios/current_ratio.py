# good above 1
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import NoContent


class CurrentRatio(StockCalculator):

    def __init__(self,current_assets,current_liabilities):
        self.current_assets = current_assets
        self.current_liabilities=current_liabilities

    async def calculate(self):
        current_ratio= self.current_assets / self.current_liabilities
        current_ratio=current_ratio.round(2).dropna()
        return current_ratio
