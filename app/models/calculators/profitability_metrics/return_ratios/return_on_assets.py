# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import NoContent


class ReturnOnAssets(StockCalculator):

    def __init__(self,net_income_common_stockholders,total_assets):
        self.net_income_common_stockholders = net_income_common_stockholders
        self.total_assets = total_assets

    def __repr__(self):
        return (f"ReturnOnAssets(net_income_common_stockholders={self.net_income_common_stockholders}, "
                f"total_assets={self.total_assets})")

    async def calculate(self):
        if self.validate_params():
            return (self.net_income_common_stockholders/self.total_assets)*100
        else:
            return (f'Error calculating net_income = {self.net_income_common_stockholders},'
             f'total_assets={self.total_assets}')

    async def validate_params(self):
        if isinstance(self.net_income_common_stockholders, float) and isinstance(self.total_assets, float):
            return True
        return False


    