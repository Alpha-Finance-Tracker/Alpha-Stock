from app.models.base_models.stock_calculator import StockCalculator


class Nopat(StockCalculator):
    def __init__(self,operating_incomes,tax_rates):
        self.operating_incomes = operating_incomes
        self.tax_rates=tax_rates


    async def calculate(self):

        nopat = self.operating_incomes * (1 - self.tax_rates / 100)
        nopat = nopat.round(2).dropna()
        return nopat