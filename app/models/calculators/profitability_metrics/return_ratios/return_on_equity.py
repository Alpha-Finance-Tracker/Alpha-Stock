# good above 5-7%

# good above 12 %

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class ReturnOnEquity(StockCalculator):

    def __init__(self, net_income_common_stockholders, stockholders_equity):
        self.net_income_common_stockholders = net_income_common_stockholders
        self.stockholders_equity = stockholders_equity

    def __repr__(self):
        return (f"ReturnOnEquity(net_income_common_stockholders={self.net_income_common_stockholders}, "
                f"stockholders_equity={self.stockholders_equity})")

    async def calculate(self):
        try:
            return (self.net_income_common_stockholders / self.stockholders_equity) * 100
        except:
            raise CalculationError()