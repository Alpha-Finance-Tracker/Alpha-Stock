

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.AI_features.ML_services import ml_stock_prediction
from app.utilities.auth_verification_services import verify_token



ML_router = APIRouter(prefix='/ML_services')
security = HTTPBearer()


@ML_router.get('/future_price')
async def stock_prediction(symbol: str,
                     credentials: HTTPAuthorizationCredentials = Depends(security)):

    await verify_token(credentials.credentials)
    return ml_stock_prediction(symbol)
