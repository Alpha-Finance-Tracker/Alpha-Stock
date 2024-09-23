from app.models.base_models.stock_calculator import StockCalculator


class Nopat(StockCalculator):
    def __init__(self,income_statement):
        self.income_statement = income_statement


    async def calculate(self,tax_rates):
        operating_incomes = self.income_statement.loc['Operating Income']

        nopat = operating_incomes * (1 - tax_rates / 100)

        nopat = nopat.round(2).dropna()
        return nopat