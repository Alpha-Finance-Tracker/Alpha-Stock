# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class ReturnOnInvestedCapital(StockCalculator):

    def __init__(self,nopat,average_invested_capital):
        self.nopat=nopat
        self.average_invested_capital=average_invested_capital
    async def calculate(self):
        if self.validate_params():
            return (self.nopat/self.average_invested_capital) * 100
        else:
            return f'Error calculating nopat={self.nopat},average_invested_capital={self.average_invested_capital}'

    async def validate_params(self):
        if isinstance(self.nopat,float) and isinstance(self.average_invested_capital,float):
            return True
        return False