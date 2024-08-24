from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.news_features.news_services import alpha_vantage_news
from app.utilities.auth_verification_services import verify_token

news_router = APIRouter(prefix='/news')
security = HTTPBearer()

@news_router.get('/')
async def stock_news(symbol:str,
               credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return alpha_vantage_news(symbol)
