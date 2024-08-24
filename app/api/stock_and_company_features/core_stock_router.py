from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.data.requests.stock_fetches import fetch_stock_minutes_av, fetch_stock_days_av, fetch_stock_weeks_av, \
    fetch_stock_latest_av
from app.api.auth_features.auth_services import get_current_user
from app.api.stock_and_company_features.core_stock_services import monthly_visualisation
from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]
stocks_router = APIRouter(prefix='/stock')


@stocks_router.get('/minutes')
async def stock_per_minute(user: user_dependency, symbol: str, minutes: int):
    stop_if_guest(user)
    return fetch_stock_minutes_av(symbol, minutes)


@stocks_router.get('/day')
async def stock_per_day(user: user_dependency, symbol: str):
    stop_if_guest(user)
    return fetch_stock_days_av(symbol)


@stocks_router.get('/week')
async def stock_per_week(user: user_dependency, symbol: str):
    stop_if_guest(user)

    return fetch_stock_weeks_av(symbol)


@stocks_router.get('/month')
async def stock_per_month(user: user_dependency, symbol: str):
    stop_if_guest(user)
    buf =  monthly_visualisation(symbol)
    return Response(content=buf.getvalue(), media_type="image/png")


@stocks_router.get('/latest')
async def stock_latest_price(user: user_dependency, symbol: str):
    stop_if_guest(user)
    return fetch_stock_latest_av(symbol)

# @stocks_router.get('/revenue')
# async def stock_revenue(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return revenue(symbol)
#
# @stocks_router.get('/debt')
# def company_debt(user: user_dependency, symbol: str):
#     stop_if_guest(user)
#     return debt(symbol)
#
# @stocks_router.get('ROE')
# def company_roe(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return roe(symbol)
#
# @stocks_router.get('EPS')
# def company_eps(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return eps(symbol)
#
