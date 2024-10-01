import pandas as pd
import pytest

from app.models.calculators.valuation.discounted_cash_flow_calculator import DiscountedCashFlow
from app.models.calculators.valuation.intrinsic_value_calculator import IntrinsicValue
from app.utilities.responses import CalculationError


@pytest.mark.asyncio
async def test_discounted_cash_flow_when_calculation_error():
    dcf = DiscountedCashFlow(latest_cash_flow=1000,
                                            discount_rate=3.5,
                                             terminal_value=None)

    with pytest.raises(CalculationError):
        await dcf.calculate()


@pytest.mark.asyncio
async def test_discounted_cash_flow_when_correct_result():
    dcf = DiscountedCashFlow(latest_cash_flow=1000,
                             discount_rate=3.5,
                             terminal_value=5.5)
    result = await dcf.calculate()

    assert isinstance(result, float)

@pytest.mark.asyncio
async def test_intrinsic_value_when_calculation_error():
    iv = IntrinsicValue(discounted_cash_flow=1000,
                                            shares_outstanding=None)

    with pytest.raises(CalculationError):
        await iv.calculate()


@pytest.mark.asyncio
async def test_intrinsic_value_when_correct_result():
    iv = IntrinsicValue(discounted_cash_flow=1000,
                        shares_outstanding=1000)
    result = await iv.calculate()

    assert isinstance(result, float)