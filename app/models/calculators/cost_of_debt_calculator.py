from app.models.base_models.stock_calculator import StockCalculator


class CostOfDebt(StockCalculator):

    def __init__(self,income_statement,balance_sheet):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet

    async def calculate(self):
        try:

            return (float(self.income_statement['interestExpense'].iloc[0]) /
                    float(self.balance_sheet['totalLiabilities'].iloc[0]))

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
