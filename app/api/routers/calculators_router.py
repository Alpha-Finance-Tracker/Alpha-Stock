from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.services.fair_value_service import FairValueService
from app.api.services.intrinsic_calculator_service import IntrinsicCalculatorService
from app.models.calculators.future_price_calculator import StockPredictor

from app.utilities.token_verification import verify_token

stock_calculator = APIRouter(prefix='/stock_calculator')

security = HTTPBearer()


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(symbol: str,
                          credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await IntrinsicCalculatorService(symbol).service()


@stock_calculator.get('/Fair_value')
async def fair_value(symbol: str,
                     credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await FairValueService(symbol).service()


@stock_calculator.get('Price_predictor')
async def stock_prediction(symbol: str,
                           credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await StockPredictor(symbol).calculate()
