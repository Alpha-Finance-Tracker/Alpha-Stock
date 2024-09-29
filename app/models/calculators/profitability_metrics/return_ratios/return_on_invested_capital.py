# good above 12 %
from app.models.base_models.basic_metric_evaluator import BasicMetricEvaluator
from app.models.base_models.stock_calculator import StockCalculator
from app.utilities.responses import CalculationError


class ReturnOnInvestedCapital(StockCalculator):

    def __init__(self,nopat,invested_capital):
        self.nopat=nopat
        self.invested_capital=invested_capital

    def __repr__(self):
        return (f"ReturnOnInvestedCapital(\n"
                f"  nopat={self.nopat},\n"
                f"  invested_capital={self.invested_capital}\n"
                f")")

    async def calculate(self):
            avg_invested_capital = (self.invested_capital + self.invested_capital.shift(1)) / 2
            print(avg_invested_capital)
            roic = (self.nopat / avg_invested_capital) * 100
            roic = roic.round(2).dropna()
            return roic
