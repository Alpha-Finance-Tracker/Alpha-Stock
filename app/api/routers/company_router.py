from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.services.company_service import CompanyService
from app.models.data_stream.alpha_vantage_data import AlphaVantage
from app.models.data_stream.yahoo_finance_data import YahooFinance
from app.utilities.token_verification import verify_token

company_router = APIRouter(prefix='/company')

security = HTTPBearer()


@company_router.get('/Yahoo_Finance_company_evaluation')
async def yahoo_finance_company_evaluation(symbol:str):

    return await CompanyService(symbol).basic_metrics()

@company_router.get('/Financial_performance')
async def company_financial_performance(symbol: str,
                                        credentials: HTTPAuthorizationCredentials = Depends(security)):
    """This method fetches information from AV and YH and registers it in the Database"""

    await verify_token(credentials.credentials)
    return await CompanyService(symbol).financial_performance()


@company_router.get('/Company_overview')
async def company_overview(symbol: str,
                           credentials: HTTPAuthorizationCredentials = Depends(security)):
    """This method fetches information from AV"""

    await verify_token(credentials.credentials)
    return await AlphaVantage(symbol).company_overview()


@company_router.get('/information')
async def company_information(symbol: str,
                              credentials: HTTPAuthorizationCredentials = Depends(security)):
    """This method is used in order to not fetch the same information from paid APIs more than once !"""

    await verify_token(credentials.credentials)
    return await CompanyService(symbol).company_info_from_db()


@company_router.get('/news')
async def stock_news(symbol: str,
                     credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await CompanyService(symbol).news()

@company_router.get('/experiment')
async def experiment(symbol:str):
    return await YFCompanyAnalysis(symbol).company_analysis()
