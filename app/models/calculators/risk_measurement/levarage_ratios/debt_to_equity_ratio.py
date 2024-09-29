# good if below  1 or 0.5
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class DebtToEquityRatio(StockCalculator):

    def __init__(self, current_liabilities, stockholders_equity):
        self.current_liabilities = current_liabilities
        self.stockholders_equity = stockholders_equity

    def __repr__(self):
        return (f"DebtToEquityRatio(current_liabilities={self.current_liabilities}, "
                f"stockholders_equity={self.stockholders_equity})")

    async def calculate(self):
        debt_to_equity = self.current_liabilities / self.stockholders_equity
        debt_to_equity = debt_to_equity.round(2).dropna()
        return debt_to_equity
