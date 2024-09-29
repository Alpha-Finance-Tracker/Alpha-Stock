
import logging
from app.utilities.responses import CalculationError


class DiscountRate:

    def __init__(self, market_value_of_equity, market_value_of_debt, total_value_of_the_company,
                 cost_of_equity, cost_of_debt, tax_rate):

        self.market_value_of_equity = market_value_of_equity  # E
        self.market_value_of_debt = market_value_of_debt  # D
        self.total_value_of_the_company = total_value_of_the_company  # V
        self.cost_of_equity = cost_of_equity  # Re
        self.cost_of_debt = cost_of_debt  # Rd
        self.tax_rate = tax_rate  # Tc


    def __repr__(self):
        return (
            f"DiscountRate(market_value_of_equity={self.market_value_of_equity},\n"
            f"               market_value_of_debt={self.market_value_of_debt},\n"
            f"               total_value_of_the_company={self.total_value_of_the_company},\n"
            f"               cost_of_equity={self.cost_of_equity},\n"
            f"               cost_of_debt={self.cost_of_debt},\n"
            f"               tax_rate={self.tax_rate})"
        )



    async def calculate(self):
        try:
            weighted_average_cost_of_capital = (
                (self.market_value_of_equity / self.total_value_of_the_company) * self.cost_of_equity +
                (self.market_value_of_debt / self.total_value_of_the_company) * self.cost_of_debt * (1 - self.tax_rate)
            )

            return round(weighted_average_cost_of_capital,2)

        except (ZeroDivisionError, ValueError, TypeError) as e:
            logging.error(f"Calculation error: {e}")
            raise CalculationError()

