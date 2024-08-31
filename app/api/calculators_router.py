from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.calculators.fair_value_calculator import FairValue
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.calculator_utilities import IntrinsicCalculatorUtilities
from app.utilities.responses import StockDataUnavailable
from app.utilities.router_utilities.calculator_utilities import intrinsic_value_calculator_service
from app.utilities.token_verification import verify_token

stock_calculator = APIRouter(prefix='/stock_calculator')

security = HTTPBearer()


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(symbol: str,
                          credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    try:
        return await IntrinsicCalculatorUtilities(symbol).present
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

