from app.models.base_models.stock_calculator import StockCalculator


class TaxRate(StockCalculator):

    def __init__(self, income_statement):

        self.income_statement = income_statement

    async def calculate(self):
        try:
            income_tax_expense = float(self.income_statement['incomeTaxExpense'].iloc[0])
            income_before_tax = float(self.income_statement['incomeBeforeTax'].iloc[0])

            return income_tax_expense / income_before_tax

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
