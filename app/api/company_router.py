from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.utilities.router_utilities.company_utilities import financial_performance, fetch_company_info_from_db
from app.utilities.token_verification import verify_token

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
    return AlphaVantage().company_overview(symbol)


@company_router.get('/information')
async def company_information(symbol: str,
                              credentials: HTTPAuthorizationCredentials = Depends(security)):

    """This method is used in order to not fetch the same information from paid APIs more than once !"""

    await verify_token(credentials.credentials)
    return await fetch_company_info_from_db(symbol.lower())
