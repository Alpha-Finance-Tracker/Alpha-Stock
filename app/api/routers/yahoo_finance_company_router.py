from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.api.services.yahoo_finance_company_service import YFCompanyAnalysis

yahoo_router = APIRouter(prefix='/yahoo_company')

security = HTTPBearer()


@yahoo_router.get('/roa')
async def return_on_assets(symbol:str):
    return await YFCompanyAnalysis(symbol).roa_service()

@yahoo_router.get('/roe')
async def return_on_equity(symbol:str):
    return await YFCompanyAnalysis(symbol).roe_service()

@yahoo_router.get('/roic')
async def return_on_equity(symbol:str):
    return await YFCompanyAnalysis(symbol).roic_service()

@yahoo_router.get('/cash_to_debt')
async def cash_to_debt(symbol:str):
    return await YFCompanyAnalysis(symbol).cash_to_debt_service()

@yahoo_router.get('/debt_to_equity')
async def debt_to_equity(symbol:str):
    return await YFCompanyAnalysis(symbol).debt_to_equity_service()

@yahoo_router.get('/interest_coverage_ratio')
async def interest_coverage_ratio(symbol:str):
    return await YFCompanyAnalysis(symbol).interest_coverage_ratio_service()