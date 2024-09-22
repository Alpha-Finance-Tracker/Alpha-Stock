from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.models.financial_metrics.current_ratio import CurrentRatio
from app.models.financial_metrics.debt_to_ebitda import DebtToEbitda
from app.models.financial_metrics.debt_to_equity_ratio import DebtToEquityRatio
from app.models.financial_metrics.interest_coverage_ratio import InterestCoverageRatio
from app.models.financial_metrics.return_on_assets import ReturnOnAssets
from app.models.financial_metrics.return_on_equity import ReturnOnEquity
from app.models.financial_metrics.return_on_invested_capital import ReturnOnInvestedCapital


class YFCompanyAnalysis:

    def __init__(self,symbol):
        self.yahoo_finance = YahooFinance(symbol)


    @property
    def roe_data(self):
        data = {
        'net_income':self.yahoo_finance.info.loc['netIncomeToCommon'],
        'shareholders_equity':self.yahoo_finance.balance_sheet.loc['Stockholders Equity'].iloc[0]}

        return data

    async def company_analysis(self):
        roe = await ReturnOnEquity(self.yahoo_finance).evaluate()
        roa = await ReturnOnAssets(self.yahoo_finance).evaluate()
        debt_to_ebitda = await DebtToEbitda(self.yahoo_finance).evaluate()
        current_ratio = await CurrentRatio(self.yahoo_finance).evaluate()
        debt_to_equity = await DebtToEquityRatio(self.yahoo_finance).evaluate()
        interest_coverage_ratio = await InterestCoverageRatio(self.yahoo_finance).evaluate()
        roic = await ReturnOnInvestedCapital(self.yahoo_finance).evaluate()
        dcf = None
        fair_value = None
        relative_value = None

        metrics = {
            "ROE": roe,
            "ROA": roa,
            "Debt to EBITDA": debt_to_ebitda,
            "Current Ratio": current_ratio,
            "Debt to Equity Ratio": debt_to_equity,
            "Interest Coverage Ratio": interest_coverage_ratio,
            "ROIC": roic,
            "DCF": dcf,
            "Fair Value": fair_value,
            "Relative Value": relative_value,
        }

        return metrics


