# good above 1

from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class CurrentRatio(StockCalculator):

    def __init__(self, current_assets, current_liabilities):
        self.current_assets = current_assets
        self.current_liabilities = current_liabilities

    def __repr__(self):
        return (f"CurrentRatio(current_assets={self.current_assets}, "
                f"current_liabilities={self.current_liabilities})")

    async def calculate(self):
        try:
            current_ratio = self.current_assets / self.current_liabilities
            current_ratio = current_ratio.round(2).dropna()
            return current_ratio
        except:
            raise CalculationError()