import uvicorn
from fastapi import FastAPI

from app.api.routers.alpha_vantage_company_router import alpha_vantage_router
from app.api.routers.calculators_router import stock_calculator
from app.api.routers.company_router import company_router
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.yahoo_finance_company_router import yahoo_router

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_calculator, tags=['Calculators'])
app.include_router(company_router, tags=['Company'])
app.include_router(yahoo_router,tags=['Yahoo Company Data'])
app.include_router(alpha_vantage_router,tags=['Alpha Vantage Company Data'])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
