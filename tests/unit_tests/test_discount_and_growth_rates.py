import pytest

from app.models.calculators.discount_and_growth_rates.discount_rate_calculator import DiscountRate
from app.utilities.responses import CalculationError


@pytest.mark.asyncio
async def test_discount_rate_when_zero_division():
    discount_rate = DiscountRate(market_value_of_equity=0,
                                 market_value_of_debt=0,
                                 total_value_of_the_company=0,
                                 cost_of_equity=0,
                                 cost_of_debt=0,
                                 tax_rate=0)

    with pytest.raises(CalculationError):
        await discount_rate.calculate()


@pytest.mark.asyncio
async def test_discount_rate_when_value_or_type_error():
    discount_rate = DiscountRate(market_value_of_equity=None,
                                 market_value_of_debt=None,
                                 total_value_of_the_company=None,
                                 cost_of_equity=None,
                                 cost_of_debt=None,
                                 tax_rate=None)

    with pytest.raises(CalculationError):
        await discount_rate.calculate()

@pytest.mark.asyncio
async def test_discount_rate_when_does_not_raise_error():
    discount_rate = DiscountRate(market_value_of_equity=5,
                                 market_value_of_debt=5,
                                 total_value_of_the_company=5,
                                 cost_of_equity=5,
                                 cost_of_debt=5,
                                 tax_rate=2.5)

    result = await discount_rate.calculate()

    assert isinstance(result,float)