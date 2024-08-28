from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.utilities.token_verification import verify_token

news_router = APIRouter(prefix='/news')
security = HTTPBearer()

@news_router.get('/')
async def stock_news(symbol:str,
               credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return AlphaVantage().news(symbol)
