import uvicorn
from fastapi import FastAPI

from app.api.AI_features.ML_router import ML_router
from app.api.calculator_features.calculators_router import stock_calculator
from app.api.stock_and_company_features.company_router import company_router
from app.api.stock_and_company_features.core_stock_router import stocks_router
from app.api.news_features.news_router import news_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(news_router, tags=['News'])
app.include_router(stocks_router, tags=['Stocks'])
app.include_router(stock_calculator, tags = ['Calculators'])
app.include_router(ML_router, tags = ['AI'])
app.include_router(company_router, tags=['Company'])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)


