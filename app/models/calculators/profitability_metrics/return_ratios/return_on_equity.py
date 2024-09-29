# good above 5-7%

# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import NoContent


class ReturnOnEquity(StockCalculator):

    def __init__(self,net_income_common_stockholders,stockholders_equity):
        self.net_income_common_stockholders = net_income_common_stockholders
        self.stockholders_equity=stockholders_equity

    def __repr__(self):
        return (f"ReturnOnEquity(net_income_common_stockholders={self.net_income_common_stockholders}, "
                f"stockholders_equity={self.stockholders_equity})")

    async def calculate(self):
        if self.validate_params():
            return (self.net_income_common_stockholders / self.stockholders_equity) * 100
        else:
            return (f'Error calculating net_income = {self.net_income_common_stockholders},'
                    f'stockholders_equity={self.stockholders_equity}')

    async def validate_params(self):
        if isinstance(self.net_income_common_stockholders,float) and isinstance(self.stockholders_equity,float):
            return True
        return False
