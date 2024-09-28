from async_lru import alru_cache
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.services.yahoo_finance_company_service import YFCompanyAnalysis
from app.utilities.timing_decorator import timeit
from app.utilities.token_verification import verify_token

yahoo_router = APIRouter(prefix='/yahoo_company')

security = HTTPBearer()


@yahoo_router.get('/roa')
@alru_cache
async def return_on_assets(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).roa_service()

@yahoo_router.get('/roe')
@alru_cache
async def return_on_equity(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).roe_service()

@yahoo_router.get('/roic')
@alru_cache
async def return_on_equity(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).roic_service()

@yahoo_router.get('/cash_to_debt')
@alru_cache
async def cash_to_debt(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).cash_to_debt_service()

@yahoo_router.get('/debt_to_equity')
@alru_cache
async def debt_to_equity(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).debt_to_equity_service()

@yahoo_router.get('/interest_coverage_ratio')
@alru_cache
async def interest_coverage_ratio(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).interest_coverage_ratio_service()

@yahoo_router.get('/current_ratio')
@alru_cache
async def current_ratio(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).current_ratio_service()

@yahoo_router.get('/debt_to_ebitda')
@alru_cache
async def debt_to_ebitda(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).debt_to_ebitda_service()

@yahoo_router.get('/gross_profit_margin')
@alru_cache
async def gross_profit_margin(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).gross_profit_margin()

@yahoo_router.get('/net_profit_margin')
@alru_cache
async def net_profit_margin(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).net_profit_margin()

@yahoo_router.get('/operating_profit_margin')
@alru_cache
async def operating_profit_margin(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).operating_profit_margin()

@yahoo_router.get('/price_valuations')
@alru_cache
async def price_valuations(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).price_valuations()

@yahoo_router.get('/fair_value')
@alru_cache
async def fair_value(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).fair_value()

@yahoo_router.get('/relative_value')
@timeit
@alru_cache
async def relative_value(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).relative_value()


@yahoo_router.get('/intrinsic_value')
@alru_cache
async def intrinsic_value(symbol:str,credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await YFCompanyAnalysis(symbol).dcf()

