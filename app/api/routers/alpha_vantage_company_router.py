from async_lru import alru_cache
from fastapi import APIRouter

from app.api.services.alpha_vantage_company_service import AVCompanyAnalysis
from app.utilities.timing_decorator import timeit

alpha_vantage_router = APIRouter(prefix='/alpha_vantage_company')




@alpha_vantage_router.get('/roa')
@timeit
@alru_cache
async def return_on_assets(symbol:str):
    return await AVCompanyAnalysis(symbol).roa_service()

@alpha_vantage_router.get('/roe')
@alru_cache
async def return_on_equity(symbol:str):
    return await AVCompanyAnalysis(symbol).roe_service()

# @alpha_vantage_router.get('/roic')
# @alru_cache
# async def return_on_equity(symbol:str):
#     return await AVCompanyAnalysis(symbol).roic_service()
#
# @alpha_vantage_router.get('/cash_to_debt')
# @alru_cache
# async def cash_to_debt(symbol:str):
#     return await YFCompanyAnalysis(symbol).cash_to_debt_service()
#
# @alpha_vantage_router.get('/debt_to_equity')
# @alru_cache
# async def debt_to_equity(symbol:str):
#     return await YFCompanyAnalysis(symbol).debt_to_equity_service()
#
# @alpha_vantage_router.get('/interest_coverage_ratio')
# @alru_cache
# async def interest_coverage_ratio(symbol:str):
#     return await YFCompanyAnalysis(symbol).interest_coverage_ratio_service()
#
# @alpha_vantage_router.get('/current_ratio')
# @alru_cache
# async def current_ratio(symbol:str):
#     return await YFCompanyAnalysis(symbol).current_ratio_service()
#
# @alpha_vantage_router.get('/debt_to_ebitda')
# @alru_cache
# async def debt_to_ebitda(symbol:str):
#     return await YFCompanyAnalysis(symbol).debt_to_ebitda_service()
#
# @alpha_vantage_router.get('/gross_profit_margin')
# @alru_cache
# async def gross_profit_margin(symbol:str):
#     return await YFCompanyAnalysis(symbol).gross_profit_margin()
#
# @alpha_vantage_router.get('/net_profit_margin')
# @alru_cache
# async def net_profit_margin(symbol:str):
#     return await YFCompanyAnalysis(symbol).net_profit_margin()
#
# @alpha_vantage_router.get('/operating_profit_margin')
# @alru_cache
# async def operating_profit_margin(symbol:str):
#     return await YFCompanyAnalysis(symbol).operating_profit_margin()
#
# @alpha_vantage_router.get('/price_valuations')
# @alru_cache
# async def price_valuations(symbol:str):
#     return await YFCompanyAnalysis(symbol).price_valuations()
#
# @alpha_vantage_router.get('/fair_value')
# @alru_cache
# async def fair_value(symbol:str):
#     return await YFCompanyAnalysis(symbol).fair_value()
#
# @alpha_vantage_router.get('/relative_value')
# @timeit
# @alru_cache
# async def relative_value(symbol:str):
#     return await YFCompanyAnalysis(symbol).relative_value()
#
#
# @alpha_vantage_router.get('/intrinsic_value')
# @alru_cache
# async def intrinsic_value(symbol:str):
#     return await YFCompanyAnalysis(symbol).dcf()
