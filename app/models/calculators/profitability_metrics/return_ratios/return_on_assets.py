# good above 12 %
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class ReturnOnAssets(StockCalculator):

    def __init__(self, net_income_common_stockholders, total_assets):
        self.net_income_common_stockholders = net_income_common_stockholders
        self.total_assets = total_assets

    def __repr__(self):
        return (f"ReturnOnAssets(net_income_common_stockholders={self.net_income_common_stockholders}, "
                f"total_assets={self.total_assets})")

    async def calculate(self):
        try:
            return (self.net_income_common_stockholders / self.total_assets) * 100
        except:
            raise CalculationError()