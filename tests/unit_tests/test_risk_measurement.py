import pytest

from app.models.calculators.risk_measurement.levarage_ratios.cash_to_debt_ratio import CashToDebtRatio
from app.models.calculators.risk_measurement.levarage_ratios.debt_to_equity_ratio import DebtToEquityRatio
from app.models.calculators.risk_measurement.levarage_ratios.interest_coverage_ratio import InterestCoverageRatio
from app.models.calculators.risk_measurement.liquidity_ratios.current_ratio import CurrentRatio
from app.models.calculators.risk_measurement.solvency_ratios.debt_to_ebitda_ratio import DebtToEbitdaRatio
from app.models.calculators.risk_measurement.solvency_ratios.tax_rate import TaxRate
from app.utilities.responses import CalculationError

from tests.mocked_data import *


@pytest.mark.asyncio
async def test_cash_to_debt_when_calculation_error():
    cash_to_debt_ratio = CashToDebtRatio(total_debt=mock_df['Total Debt'],
                                         cash_and_cash_equivalents=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await cash_to_debt_ratio.calculate()


@pytest.mark.asyncio
async def test_cash_to_debt_when_correct_result():
    cash_to_debt_ratio = CashToDebtRatio(total_debt=mock_df['Total Debt'],
                                         cash_and_cash_equivalents=mock_df['Cash and Cash Equivalents'])

    result = await cash_to_debt_ratio.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_debt_to_equity_ratio_calculation_error():
    debt_to_equity_ratio = DebtToEquityRatio(current_liabilities=mock_df['Current Liabilities'],
                                             stockholders_equity=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await debt_to_equity_ratio.calculate()


@pytest.mark.asyncio
async def test_debt_to_equity_ratio_when_correct_result():
    debt_to_equity_ratio = DebtToEquityRatio(current_liabilities=mock_df['Current Liabilities'],
                                             stockholders_equity=mock_df['Stockholders Equity'])
    result = await debt_to_equity_ratio.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_interest_coverage_ratio_calculation_error():
    interest_coverage_ratio = InterestCoverageRatio(ebit=mock_df['EBIT'],
                                                    interest_expense=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await interest_coverage_ratio.calculate()


@pytest.mark.asyncio
async def test_interest_coverage_ratio_when_correct_result():
    interest_coverage_ratio = InterestCoverageRatio(ebit=mock_df['EBIT'],
                                                    interest_expense=mock_df['Interest Expense'])
    result = await interest_coverage_ratio.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_interest_coverage_ratio_calculation_error():
    current_ratio = CurrentRatio(current_assets=mock_df['Current Assets'],
                                 current_liabilities=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await current_ratio.calculate()


@pytest.mark.asyncio
async def test_current_ratio_when_correct_result():
    current_ratio = CurrentRatio(current_assets=mock_df['Current Assets'],
                                 current_liabilities=mock_df['Current Liabilities'])
    result = await current_ratio.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_debt_to_ebitda_ratio_when_calculation_error():
    debt_to_ebitda_ratio = DebtToEbitdaRatio(ebitda=mock_df['EBITDA'],
                                      total_debt=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await debt_to_ebitda_ratio.calculate()


@pytest.mark.asyncio
async def test_debt_to_ebitda_ratio_when_correct_result():
    debt_to_ebitda_ratio = DebtToEbitdaRatio(ebitda=mock_df['EBITDA'],
                                      total_debt=mock_df['Total Debt'])

    result = await debt_to_ebitda_ratio.calculate()
    assert isinstance(result, pd.Series)

@pytest.mark.asyncio
async def test_tax_rate_when_calculation_error():
    tax_rate = TaxRate(income_before_tax=mock_df['Income Before Tax'],
                                      income_after_tax=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await tax_rate.calculate()


@pytest.mark.asyncio
async def test_tax_rate_when_correct_result():
    tax_rate = TaxRate(income_before_tax=mock_df['Income Before Tax'],
                                      income_after_tax=mock_df['Income After Tax'])

    result = await tax_rate.calculate()
    assert isinstance(result, pd.Series)
