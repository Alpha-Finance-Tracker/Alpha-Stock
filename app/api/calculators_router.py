from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.calculators.fair_value_calculator import FairValue
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.router_utilities.calculator_utilities import intrinsic_value_calculator_service
from app.utilities.token_verification import verify_token

stock_calculator = APIRouter(prefix='/stock_calculator')

security = HTTPBearer()


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(symbol: str,
                          credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await intrinsic_value_calculator_service(symbol)


@stock_calculator.get('/peter_lynch_fair_price')
async def peter_lynch(symbol:str,
                      credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return FairValue(symbol).calculate()

@stock_calculator.get('/test')
async def test(symbol:str,
                      credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return {'data1':YahooFinance(symbol).balance_sheet,
            'data2':AlphaVantage(symbol).balance_sheet()}


