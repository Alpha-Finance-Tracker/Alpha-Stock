import pandas as pd

"""Assumption variables
    1. Terminal growth Rate
    2. Discount rate (WACC)
    3. Projection Period
    4. Growth Rates During Projection Period
    5. Tax Rate
    6. Capital Expenditures (CapEx)
    """


class AlphaStock:
    def __init__(self, **kwargs):
        self.symbol = kwargs.get('symbol', None)
        self.income_statement = kwargs.get('income_statement', None)
        self.balance_sheet = kwargs.get('balance_sheet', None)
        self.annual_eps = kwargs.get('annual_eps', None)
        self.cash_flows = kwargs.get('cash_flows', None)
        self.co = kwargs.get('co', None)  # company overview
        self.market_data_info = kwargs.get('market_data', None)
        self.competitors_pe_ratio = kwargs.get('competitors_pe_ratio', None)

    @property
    def revenue(self):
        try:
            self.income_statement['fiscalDateEnding'] = pd.to_datetime(self.income_statement['fiscalDateEnding'])
            self.income_statement['totalRevenue'] = pd.to_numeric(self.income_statement['totalRevenue'],
                                                                  errors='coerce')
            self.income_statement['growth_rate'] = self.income_statement[
                                                       'totalRevenue'].pct_change() * 100  # Calculate and convert to percentage
            self.income_statement['growth_rate'] = self.income_statement['growth_rate'].fillna(0)

            data = self.income_statement[['growth_rate', 'fiscalDateEnding']]

            return data

        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def debt(self):
        try:
            result = self.balance_sheet[['currentDebt', 'fiscalDateEnding']]
            self.balance_sheet['currentDebt'] = self.balance_sheet['currentDebt'].fillna(0)

            return result
        except Exception as e:
            print(f"Error calculating debt level: {e}")
            return None

    @property
    def net_income(self):
        try:
            data = self.income_statement[['fiscalDateEnding', 'netIncome']]
            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def eps(self):
        try:
            data = self.annual_eps[['fiscalDateEnding', 'reportedEPS']]
            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def net_profit_margin(self):
        try:
            self.income_statement['netProfitMargin'] = (pd.to_numeric(self.income_statement['netIncome'],
                                                                      errors='coerce') / pd.to_numeric(
                self.income_statement['totalRevenue'], errors='coerce')) * 100

            self.income_statement['netProfitMargin'] = self.income_statement['netProfitMargin'].pct_change() * 100

            net_profit = self.income_statement[['netProfitMargin', 'fiscalDateEnding']]

            return net_profit
        except Exception as e:
            print(f"Error with net_profit_margin {e}")
            return None

    @property
    def roe(self):
        try:

            self.balance_sheet['shareholdersEquity'] = (
                    pd.to_numeric(self.balance_sheet['totalAssets'], errors='coerce') - pd.to_numeric(
                self.balance_sheet['totalLiabilities'], errors='coerce'))
            self.balance_sheet['roe'] = (
                    pd.to_numeric(self.income_statement['netIncome'], errors='coerce') - self.balance_sheet[
                'shareholdersEquity'])

            roe = self.balance_sheet[['fiscalDateEnding', 'roe']]
            return roe

        except Exception as e:
            print(f"Error with roe: {e}")
            return None

    @property
    def cash(self):
        try:

            return self.cash_flows[['fiscalDateEnding', 'operatingCashflow']]
        except Exception as e:
            print(f"Error with cash method: {e}")
            return None

    # @property
    # def change_in_nwc(self):  # net work capital
    #     this_year_assets = float(self.balance_sheet.iloc[0]['totalCurrentAssets'])
    #     last_year_assets = float(self.balance_sheet.iloc[1]['totalCurrentAssets'])
    #     this_year_liabilities = float(self.balance_sheet.iloc[0]['totalCurrentLiabilities'])
    #     last_year_liabilities = float(self.balance_sheet.iloc[1]['totalCurrentLiabilities'])
    #
    #     latest_nwc = this_year_assets - this_year_liabilities
    #     last_year_nwc = last_year_assets - last_year_liabilities
    #
    #     return latest_nwc - last_year_nwc

    @property
    def dcf(self):
        try:
            fcf = float(self.cash_flows.loc['Free Cash Flow'][0])
            discount_rate = self.discount_rate
            terminal_growth_rate = 0.03
            terminal_value = fcf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)

            projection_years = 5  # This is an assumption
            dcf = (sum([(fcf / (1 + discount_rate) ** year) for year in range(1, projection_years + 1)])
                   + (terminal_value / (1 + discount_rate) ** projection_years))

            return dcf
        except Exception as e:
            print(f"Error calculating discounted cash flows: {e}")
            return None

    @property
    def discount_rate(self):
        try:
            risk_rate = 0.03  # This is an assumption
            market_return = self.calculate_market_data
            beta = 1 if self.co['Beta'] is None else float(self.co['Beta'])

            cost_of_debt = float(self.income_statement['interestExpense'].iloc[0]) / float(
                self.balance_sheet['totalLiabilities'].iloc[0])

            debt_ratio = float(self.balance_sheet['totalLiabilities'].iloc[0]) / (
                    float(self.balance_sheet['totalLiabilities'].iloc[0]) + float(
                self.balance_sheet['totalShareholderEquity'].iloc[0]))

            equity_ratio = float(self.balance_sheet['totalShareholderEquity'].iloc[0]) / (
                    float(self.balance_sheet['totalLiabilities'].iloc[0]) + float(
                self.balance_sheet['totalShareholderEquity'].iloc[0]))

            total_market_value = equity_ratio + debt_ratio
            cost_of_equity = risk_rate + beta * (market_return - risk_rate)

            tax_rate = float(self.income_statement['incomeTaxExpense'].iloc[0]) / float(
                self.income_statement['incomeBeforeTax'].iloc[0])

            wacc = (equity_ratio / total_market_value) * cost_of_equity + (
                    debt_ratio / total_market_value) * cost_of_debt * (1 - tax_rate)
            return wacc
        except Exception as e:
            print(f"Error calculating discount rate: {e}")
            return None

    @property
    def calculate_market_data(self):
        try:
            # Ensure 'Adj Close' column exists and data is not empty
            if 'Adj Close' not in self.market_data_info.columns or self.market_data_info.empty:
                raise ValueError("Missing 'Adj Close' column or data is empty.")
            self.market_data_info['daily_return'] = self.market_data_info['Adj Close'].pct_change()
            daily_returns = self.market_data_info['daily_return'].dropna()
            average_daily_return = daily_returns.mean()
            average_market_return = average_daily_return * 252

            return average_market_return

        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None

    @property
    def calculate_intrinsic_value_per_share(self):

        """This method calculates the intrinsic value per share based on the total discounted cash flows from the dcf method."""

        try:
            dcf = self.dcf
            so = float(self.co['SharesOutstanding'])
            return dcf / so
        except Exception as e:
            print(f"Error calculating intrinsic value : {e}")
            return None

    @property
    def calculate_relative_value_per_share(self):
        return (sum(self.competitors_pe_ratio) // len(self.competitors_pe_ratio)) * float(self.co['EPS'])
