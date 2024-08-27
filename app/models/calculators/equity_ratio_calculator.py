from app.models.base_models.stock_calculator import StockCalculator


class EquityRatio(StockCalculator):

    def __init__(self, balance_sheet):

        self.balance_sheet = balance_sheet

    def calculate(self):
        try:
            total_liabilities = float(self.balance_sheet['totalLiabilities'].iloc[0])
            total_shareholder_equity = float(self.balance_sheet['totalShareholderEquity'].iloc[0])

            return total_shareholder_equity / (total_liabilities + total_shareholder_equity)

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None
