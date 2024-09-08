import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.api.routers.calculators_router import stock_calculator
from app.utilities.responses import AlphaVantageAPIKey, AlphaVantageNoData, CalculationError
from tests.mocked_data import *

app = FastAPI()
app.include_router(stock_calculator)


@pytest.mark.asyncio
async def test_intrinsic_value_flow__when_token_invalid():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_data_stream_service_results_in_API_KEY_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(side_effect=AlphaVantageAPIKey))
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 429
        assert response.json()['detail'] == 'Alpha Vantage daily API fetch limit(25) exceeded.!'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_data_stream_service_results_in_absent_data_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(side_effect=AlphaVantageNoData))
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 404
        assert response.json()['detail'] == 'Alpha Vantage does not have information about the stock'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_discount_rate_results_in_calculation_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(return_value=mock_intrinsic_ds_data))

    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.calculate',
                 mocker.AsyncMock(side_effect=CalculationError))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 500
        assert response.json()['detail'] == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_discounted_cash_flow_results_in_calculation_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(return_value=mock_intrinsic_ds_data))

    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.calculate',
                 mocker.AsyncMock(side_effect=CalculationError))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 500
        assert response.json()['detail'] == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_relative_value_results_in_calculation_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(return_value=mock_intrinsic_ds_data))

    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.relative_value_calculator.RelativeValue.calculate',
                 mocker.AsyncMock(side_effect=CalculationError))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 500
        assert response.json()['detail'] == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_when_intrinsic_value_results_in_calculation_error(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(return_value=mock_intrinsic_ds_data))

    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.relative_value_calculator.RelativeValue.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.intrinsic_value_calculator.IntrinsicValue.calculate',
                 mocker.AsyncMock(side_effect=CalculationError))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 500
        assert response.json()['detail'] == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_intrinsic_value_flow_successfully(mocker):
    mocker.patch('app.models.data_stream.intrinsic_value_ds.IntrinsicValueDS.unload',
                 mocker.AsyncMock(return_value=mock_intrinsic_ds_data))

    mocker.patch('app.models.calculators.discount_rate_calculator.DiscountRate.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.discounted_cash_flow_calculator.DiscountedCashFlow.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.relative_value_calculator.RelativeValue.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    mocker.patch('app.models.calculators.intrinsic_value_calculator.IntrinsicValue.calculate',
                 mocker.AsyncMock(return_value=mock_valid_return))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Intrinsic_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_fair_value_calculator_flow_when_token_invalid():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Fair_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_fair_value_calculator_flow_when_invalid_data_gets_in(mocker):
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.price_to_earnings_ratio',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.dividend_yield',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.earnings_per_share_growth_rate',
                 mocker.PropertyMock(return_value=mock_invalid_return))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Fair_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

    assert response.status_code == 500
    assert response.json()['detail'] == 'Oops, Calculation error occurred.'

@pytest.mark.asyncio
async def test_fair_value_calculator_flow_when_invalid_data_gets_in(mocker):
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.price_to_earnings_ratio',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.dividend_yield',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.earnings_per_share_growth_rate',
                 mocker.PropertyMock(return_value=mock_invalid_return))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Fair_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

    assert response.status_code == 500
    assert response.json()['detail'] == 'Oops, Calculation error occurred.'


@pytest.mark.asyncio
async def test_fair_value_calculator_flow_successfully(mocker):
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.price_to_earnings_ratio',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.dividend_yield',
                 mocker.PropertyMock(return_value=mock_valid_return))
    mocker.patch('app.models.calculators.fair_value_calculator.FairValue.earnings_per_share_growth_rate',
                 mocker.PropertyMock(return_value=mock_valid_return))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/stock_calculator/Fair_value', params=mock_symbol,
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

    assert response.status_code == 200
