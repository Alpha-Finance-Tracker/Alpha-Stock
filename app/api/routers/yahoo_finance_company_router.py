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