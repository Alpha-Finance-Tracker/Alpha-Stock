
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.calculators.future_price_calculator import StockPredictor
from app.utilities.token_verification import verify_token

AI_router = APIRouter(prefix='/ML_services')
security = HTTPBearer()


@AI_router.get('/future_price')
async def stock_prediction(symbol: str,
                           credentials: HTTPAuthorizationCredentials = Depends(security)):

    await verify_token(credentials.credentials)
    return StockPredictor(symbol).calculate()
