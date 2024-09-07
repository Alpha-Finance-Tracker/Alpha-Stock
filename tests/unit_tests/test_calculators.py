

import pytest

from app.models.calculators.cost_of_debt_calculator import CostOfDebt
from app.models.calculators.cost_of_equity_calculator import CostOfEquity
from app.models.calculators.debt_ratio_calculator import DebtRatio
from app.models.calculators.discount_rate_calculator import DiscountRate
from app.models.calculators.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.equity_ratio_calculator import EquityRatio
from app.models.calculators.fair_value_calculator import FairValue
from app.models.calculators.intrinsic_value_calculator import IntrinsicValue
from app.models.calculators.relative_value_calculator import RelativeValue
from app.models.calculators.tax_rate_calculator import TaxRate
from app.models.calculators.terminal_value_calculator import TerminalValue
from app.models.calculators.total_market_value_calculator import TotalMarketValue
from app.utilities.responses import CalculationError


@pytest.mark.asyncio
async def test_cost_of_debt_calculator_when_invalid_data_gets_in(mocker):
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.last_year_interest_expense',
                 mocker.PropertyMock(return_value='a'))
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.last_year_total_liabilities',
                 mocker.PropertyMock(return_value=0))


    with pytest.raises(CalculationError) as exc_info:
        await CostOfDebt(None, None).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_cost_of_debt_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.last_year_interest_expense',
                 mocker.PropertyMock(return_value=4))
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.last_year_total_liabilities',
                 mocker.PropertyMock(return_value=2))

    result = await CostOfDebt(None, None).calculate()

    assert isinstance(result,float)




@pytest.mark.asyncio
async def test_cost_of_equity_calculator_when_data_is_invalid():
    with pytest.raises(CalculationError) as exc_info:
        await CostOfEquity('a',2,10).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_cost_of_equity_calculator_when_data_is_valid():
    result = await CostOfEquity(5.1, 2, 10).calculate()
    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_debt_ratio_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.last_year_total_liabilities',
                 mocker.PropertyMock(return_value='a'))
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.last_year_total_shareholder_equity',
                 mocker.PropertyMock(return_value=0))


    with pytest.raises(CalculationError) as exc_info:
        await DebtRatio(None).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_debt_ratio_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.last_year_total_liabilities',
                 mocker.PropertyMock(return_value=5))
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.last_year_total_shareholder_equity',
                 mocker.PropertyMock(return_value=10.5))



    result = await DebtRatio(None).calculate()

    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_discount_rate_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.beta',
                 mocker.PropertyMock(return_value=1))
    mocker.patch('app.models.calculators.market_data_calculator.AverageMarketData.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.cost_of_equity_calculator.CostOfEquity.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.calculate',
                 mocker.AsyncMock(return_value='a'))
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.total_market_value_calculator.TotalMarketValue.calculate',
                 mocker.AsyncMock(return_value=20))



    with pytest.raises(CalculationError) as exc_info:
        await DiscountRate(None,None,
                           None,None,None).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_discount_rate_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.beta',
                 mocker.PropertyMock(return_value=1))
    mocker.patch('app.models.calculators.market_data_calculator.AverageMarketData.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.cost_of_debt_calculator.CostOfDebt.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.cost_of_equity_calculator.CostOfEquity.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.debt_ratio_calculator.DebtRatio.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.calculate',
                 mocker.AsyncMock(return_value=20))
    mocker.patch('app.models.calculators.total_market_value_calculator.TotalMarketValue.calculate',
                 mocker.AsyncMock(return_value=20.1))

    result = await DiscountRate(None,None,
                           None,None,None).calculate()

    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_discounted_cash_flow_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.last_year_free_cash_flow',
                 mocker.PropertyMock(return_value='a'))
    mocker.patch('app.models.calculators.terminal_value_calculator.TerminalValue.calculate',
                 mocker.AsyncMock(return_value=10))

    with pytest.raises(CalculationError) as exc_info:
        await DiscountedCashFlow(None,2).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'



@pytest.mark.asyncio
async def test_discounted_cash_flow_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.last_year_free_cash_flow',
                 mocker.PropertyMock(return_value=10))
    mocker.patch('app.models.calculators.terminal_value_calculator.TerminalValue.calculate',
                 mocker.AsyncMock(return_value=10.5))


    result = await DiscountedCashFlow(None,2).calculate()
    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_equity_ratio_calculator_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.last_year_total_liabilities',
                 mocker.PropertyMock(return_value='a'))
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.last_year_total_shareholder_equity',
                 mocker.PropertyMock(return_value=10.5))

    with pytest.raises(CalculationError) as exc_info:
        await EquityRatio(None).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_equity_ratio_calculator_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.last_year_total_liabilities',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.equity_ratio_calculator.EquityRatio.last_year_total_shareholder_equity',
                 mocker.PropertyMock(return_value=10.5))


    result = await EquityRatio(None).calculate()
    assert isinstance(result,float)


@pytest.mark.asyncio
async def test_fair_value_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.price_to_earnings_ratio',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.dividend_yield',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.earnings_per_share_growth_rate',
                 mocker.PropertyMock(return_value='a'))

    with pytest.raises(CalculationError) as exc_info:
        await FairValue('symbol').calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_fair_value__calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.price_to_earnings_ratio',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.dividend_yield',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.earnings_per_share_growth_rate',
                 mocker.PropertyMock(return_value=10.5))

    result = await FairValue('symbol').calculate()
    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_intrinsic_value_calculator_when_data_is_invalid():

    with pytest.raises(CalculationError) as exc_info:
        await IntrinsicValue(0,'a').calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_intrinsic_value_calculator_when_data_is_valid():
    result = await IntrinsicValue(8.5,5).calculate()
    assert isinstance(result,float)


@pytest.mark.asyncio
async def test_relative_value_calculator_when_data_is_invalid():
    with pytest.raises(CalculationError) as exc_info:
        await RelativeValue([]).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_relative_value_calculator_when_data_is_valid():
    result = await RelativeValue([4,4,4]).calculate()

    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_tax_rate_calculator_when_data_is_invalid(mocker):
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.last_year_income_tax_expense',
                 mocker.PropertyMock(return_value=0))
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.last_year_income_before_tax',
                 mocker.PropertyMock(return_value='a'))

    with pytest.raises(CalculationError) as exc_info:
        await TaxRate(None).calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_tax_rate_calculator_when_data_is_valid(mocker):
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.last_year_income_tax_expense',
                 mocker.PropertyMock(return_value=10.5))
    mocker.patch('app.models.calculators.tax_rate_calculator.TaxRate.last_year_income_before_tax',
                 mocker.PropertyMock(return_value=10.5))


    result = await TaxRate(None).calculate()
    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_terminal_value_calculator_when_data_is_invalid():
    with pytest.raises(CalculationError) as exc_info:
        await TerminalValue(10.5,10.5,'a').calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_terminal_value_calculator_when_data_is_valid():

    result = await TerminalValue(10.5,10.5,100.5).calculate()

    assert isinstance(result,float)

@pytest.mark.asyncio
async def test_total_market_value_calculator_when_data_is_invalid():
    with pytest.raises(CalculationError) as exc_info:
        await TotalMarketValue(10.5,'a').calculate()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_total_market_value_calculator_when_data_is_valid():

    result = await TotalMarketValue(10.5,10.5).calculate()

    assert isinstance(result,float)

