from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.services.calculator_service import IntrinsicValueService
from app.models.calculators.fair_value_calculator import FairValue
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.responses import StockDataUnavailable

from app.utilities.token_verification import verify_token

stock_calculator = APIRouter(prefix='/stock_calculator')

security = HTTPBearer()


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(symbol: str,
                          credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    try:
        return await IntrinsicValueService(symbol).service()

    except StockDataUnavailable as e :
        raise e


@stock_calculator.get('/peter_lynch_fair_price')
async def peter_lynch(symbol:str,
                      credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)

    try:
        return FairValue(symbol).calculate()
    except StockDataUnavailable as e :
        raise e


@stock_calculator.get('/test')
async def test(symbol):
    return YahooFinance(symbol).cash_flow

