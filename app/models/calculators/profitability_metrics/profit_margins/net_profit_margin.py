from app.models.base_models.stock_calculator import StockCalculator


class NetProfitMargin(StockCalculator):

    def __init__(self,net_incomes,total_revenues):
        self.net_incomes=net_incomes
        self.total_revenues=total_revenues

    def __repr__(self):
        return (f"NetProfitMargin(net_incomes={self.net_incomes}, "
                f"total_revenues={self.total_revenues})")

    async def calculate(self):
        net_profit_margin = (self.net_incomes / self.total_revenues) * 100
        net_profit_margin=net_profit_margin.round(2).dropna()
        return net_profit_margin
