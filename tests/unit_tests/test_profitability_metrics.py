import pytest

from app.models.calculators.profitability_metrics.profit_margins.gross_profit_margin import GrossProfitMargin
from app.models.calculators.profitability_metrics.profit_margins.net_profit_margin import NetProfitMargin
from app.models.calculators.profitability_metrics.profit_margins.operating_profit_margin import OperatingProfitMargin
from app.models.calculators.profitability_metrics.return_ratios.nopat import Nopat
from app.models.calculators.profitability_metrics.return_ratios.return_on_assets import ReturnOnAssets
from app.models.calculators.profitability_metrics.return_ratios.return_on_equity import ReturnOnEquity
from app.models.calculators.profitability_metrics.return_ratios.return_on_invested_capital import \
    ReturnOnInvestedCapital
from app.utilities.responses import CalculationError
from tests.mocked_data import *


@pytest.mark.asyncio
async def test_gross_profit_margin_when_calculation_error():
    gross_profit_margin = GrossProfitMargin(gross_profits=mock_df['Gross Profit'],
                                            total_revenues=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await gross_profit_margin.calculate()


@pytest.mark.asyncio
async def test_gross_profit_margin_correct_result():
    gross_profit_margin = GrossProfitMargin(gross_profits=mock_df['Gross Profit'],
                                            total_revenues=mock_df['Total Revenue'])

    result = await gross_profit_margin.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_net_profit_margin_when_calculation_error():
    net_profit_margin = NetProfitMargin(net_incomes=mock_df['Net Incomes'],
                                        total_revenues=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await net_profit_margin.calculate()


@pytest.mark.asyncio
async def test_net_profit_margin_correct_result():
    net_profit_margin = NetProfitMargin(net_incomes=mock_df['Net Incomes'],
                                        total_revenues=mock_df['Total Revenue'])

    result = await net_profit_margin.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_operating_profit_margin_when_calculation_error():
    operating_profit_margin = OperatingProfitMargin(operating_incomes=mock_df['Operating Incomes'],
                                                    total_revenues=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await operating_profit_margin.calculate()


@pytest.mark.asyncio
async def test_operating_profit_margin_correct_result():
    operating_profit_margin = OperatingProfitMargin(operating_incomes=mock_df['Operating Incomes'],
                                                    total_revenues=mock_df['Total Revenue'])

    result = await operating_profit_margin.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_nopat_when_calculation_error():
    nopat = Nopat(operating_incomes=mock_df['Operating Incomes'],
                  tax_rates=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await nopat.calculate()


@pytest.mark.asyncio
async def test_nopat_correct_result():
    nopat = Nopat(operating_incomes=mock_df['Operating Incomes'],
                  tax_rates=mock_df['Tax Rates'])

    result = await nopat.calculate()

    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_return_on_assets_when_calculation_error():
    roa = ReturnOnAssets(net_income_common_stockholders=mock_df['Net Income Common Stockholders'],
                         total_assets=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await roa.calculate()


@pytest.mark.asyncio
async def test_return_on_assets_correct_result():
    roa = ReturnOnAssets(net_income_common_stockholders=mock_df['Net Income Common Stockholders'],
                         total_assets=mock_df['Total Assets'])

    result = await roa.calculate()
    assert isinstance(result, pd.Series)


@pytest.mark.asyncio
async def test_return_on_equity_when_calculation_error():
    roe = ReturnOnEquity(net_income_common_stockholders=mock_df['Net Income Common Stockholders'],
                         stockholders_equity=mock_df['Invalid'])

    with pytest.raises(CalculationError):
        await roe.calculate()


@pytest.mark.asyncio
async def test_return_on_equity_correct_result():
    roa = ReturnOnEquity(net_income_common_stockholders=mock_df['Net Income Common Stockholders'],
                         stockholders_equity=mock_df['Stockholders Equity'])

    result = await roa.calculate()
    assert isinstance(result, pd.Series)


# @pytest.mark.asyncio
# async def test_return_on_invested_capital_when_calculation_error():
#     roic = ReturnOnInvestedCapital(nopat=mock_df['NOPAT'],
#                          invested_capital=mock_df['Invalid'])
#
#     result = await roic.calculate()
#     assert  [] == result
#     # with pytest.raises(CalculationError):
#     #     await roic.calculate()


@pytest.mark.asyncio
async def test_return_on_invested_capital_correct_result():
    roic = ReturnOnInvestedCapital(nopat=mock_df['Net Income Common Stockholders'],
                                   invested_capital=mock_df['Invested Capital'])

    result = await roic.calculate()
    assert isinstance(result, pd.Series)
