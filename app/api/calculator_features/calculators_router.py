from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.calculator_features.calculators_services import intrinsic_value_calculator_service
from app.models.calculators.fair_value_calculator import FairValue
from app.utilities.auth_verification_services import verify_token

stock_calculator = APIRouter(prefix='/stock_calculator')

security = HTTPBearer()


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(symbol: str,
                          credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return await intrinsic_value_calculator_service(symbol)


@stock_calculator.get('/peter_lynch_fair_price')
async def peter_lynch(earnings_per_share_growth_rate: float,
                      dividend_yield: float,
                      price_to_earnings_ratio: float,
                      credentials: HTTPAuthorizationCredentials = Depends(security)):
    await verify_token(credentials.credentials)
    return FairValue(earnings_per_share_growth_rate, dividend_yield, price_to_earnings_ratio)
