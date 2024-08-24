
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.data.requests.stock_fetches import fetch_company_overview_av
from app.api.stock_and_company_features.company_services import financial_performance, fetch_company_info_from_db
from fastapi.responses import StreamingResponse

from app.utilities.auth_verification_services import verify_token

company_router = APIRouter(prefix='/company')

security = HTTPBearer()

@company_router.get('/Financial_performance')
async def company_financial_performance(symbol: str,
                                        credentials: HTTPAuthorizationCredentials = Depends(security)):

    await verify_token(credentials.credentials)
    fp = await financial_performance(symbol.lower())
    return fp


@company_router.get('/Company_overview')
async def company_overview(symbol: str,
                           credentials: HTTPAuthorizationCredentials = Depends(security)):

    await verify_token(credentials.credentials)
    co = fetch_company_overview_av(symbol.lower())
    return co


@company_router.get('/information')
async def company_information(symbol: str,
                        credentials: HTTPAuthorizationCredentials = Depends(security)):

    await verify_token(credentials.credentials)
    ci = fetch_company_info_from_db(symbol.lower())
    return StreamingResponse(ci, media_type="image/png")
