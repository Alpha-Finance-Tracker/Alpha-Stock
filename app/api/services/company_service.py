import asyncio

from fastapi.responses import StreamingResponse

from app.database.models.company import Company
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.company_data import send_parameters_towards_the_database
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.models.statements_and_reports.cash_flows import CashFlow
from app.models.statements_and_reports.debt import Debt
from app.models.statements_and_reports.earnings_per_share import EarningsPerShare
from app.models.statements_and_reports.net_income import NetIncome
from app.models.statements_and_reports.net_profit_margin import NetProfitMargin
from app.models.statements_and_reports.return_on_equity import ReturnOnEquity
from app.models.statements_and_reports.revenue_growth import RevenueGrowth

import matplotlib.pyplot as plt
import io


class CompanyService:

    def __init__(self, symbol):
        self.symbol = symbol
        self.alpha_vantage = AlphaVantage(symbol)
        self.yahoo_finance = YahooFinance(symbol)

    async def company_overview(self):
        pass

    async def basic_metrics(self):


        debt_to_ebitda = await DebtToEbitda(self.yahoo_finance).evaluate()
        roe = await ReturnOnAssets(self.yahoo_finance).evaluate()
        roa = await ReturnOnEquityYF(self.yahoo_finance).evaluate()
        current_ratio = await CurrentRatio(self.yahoo_finance).evaluate()
        debt_to_equity = await DebtToEquityRatio(self.yahoo_finance).evaluate()
        interest_coverage_ratio = await InterestCoverageRatio(self.yahoo_finance).evaluate()
        roic = await ReturnOnInvestedCapital(self.yahoo_finance).evaluate()

        return {
                'debt_to_ebitda_ratio': debt_to_ebitda,
                'roe_%': roe,
                'roa_%': roa,
                'current_ratio': current_ratio,
                'debt_to_equity_ratio': debt_to_equity,
                'interest_coverage_ratio': interest_coverage_ratio,
                'roic_%': roic}

    async def financial_performance(self):
        income_statement, balance_sheet, annual_eps, cash_flow = await asyncio.gather(
            self.alpha_vantage.income_statement(),
            self.alpha_vantage.balance_sheet(),
            self.alpha_vantage.company_earnings(),
            self.alpha_vantage.cash_flows()

        )

        (revenue_growth, net_income, earnings_per_share, return_on_equity, net_profit_margin, debt_level,
         cash_flow_parsed) = (
            RevenueGrowth(balance_sheet, income_statement).info(),
            NetIncome(income_statement).info(),
            EarningsPerShare(annual_eps).info(),
            ReturnOnEquity(balance_sheet, income_statement).info(),
            NetProfitMargin(income_statement).info(),
            Debt(balance_sheet).info(),
            CashFlow(cash_flow).info())

        await send_parameters_towards_the_database(revenue_growth,
                                                   net_income,
                                                   earnings_per_share,
                                                   return_on_equity,
                                                   debt_level,
                                                   cash_flow_parsed,
                                                   self.symbol)
        return 'Parameters successfully fetched and registered'

    async def company_info_from_db(self):
        data = await Company().view(self.symbol)
        img = await self.display_charts(data)
        return StreamingResponse(img, media_type="image/png")

    async def display_charts(self, data):
        # Extract the data from the input
        years = [x.year for x in data]
        revenue_growth = [x.revenue_growth for x in data]  # % based
        net_income = [x.net_income for x in data]
        cash_flow = [x.cash_flow for x in data]
        debt_level = [x.debt_level for x in data]
        eps = [x.eps for x in data]
        roe = [x.roe for x in data]

        # Create a figure and a set of subplots
        fig, axs = plt.subplots(3, 2, figsize=(14, 10), facecolor='none')

        # Plot data on each subplot
        axs[0, 0].plot(years, revenue_growth, 'b-o')
        axs[0, 0].set_title('Revenue Growth')
        axs[0, 0].set_xlabel('Year')
        axs[0, 0].set_ylabel('Revenue $')

        axs[0, 1].plot(years, net_income, 'r-o')
        axs[0, 1].set_title('Net Income')
        axs[0, 1].set_xlabel('Year')
        axs[0, 1].set_ylabel('Net Income $')

        axs[1, 0].plot(years, cash_flow, 'g-o')
        axs[1, 0].set_title('Cash Flow')
        axs[1, 0].set_xlabel('Year')
        axs[1, 0].set_ylabel('Cash Flow $')

        axs[1, 1].plot(years, debt_level, 'y-o')
        axs[1, 1].set_title('Debt Level')
        axs[1, 1].set_xlabel('Year')
        axs[1, 1].set_ylabel('Debt Level $')

        axs[2, 0].plot(years, eps, 'm-o')
        axs[2, 0].set_title('Earnings Per Share (EPS)')
        axs[2, 0].set_xlabel('Year')
        axs[2, 0].set_ylabel('EPS ($)')

        axs[2, 1].plot(years, roe, 'c-o')
        axs[2, 1].set_title('Return on Equity (ROE)')
        axs[2, 1].set_xlabel('Year')
        axs[2, 1].set_ylabel('ROE (%)')

        # Add some space between the subplots
        plt.tight_layout()

        # Save the figure to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True)
        img.seek(0)

        return img

    async def news(self):
        try:
            data = await self.alpha_vantage.news()

            times = [(x[0:4] + " " + x[4:6] + "." + x[6:8]) for x in data['time_published']]
            news = {'Title': data['title'],
                    'Url': data['url'],
                    'Time': times,
                    'Image': data['banner_image']}

            return news
        except Exception as e:
            return f'Error with parsing data from AV, probably fetch limit related {e}'
