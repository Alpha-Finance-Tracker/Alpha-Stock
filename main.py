import uvicorn
from fastapi import FastAPI

from app.api.routers.AI_router import AI_router
from app.api.routers.calculators_router import stock_calculator
from app.api.routers.company_router import company_router
from app.api.routers.news_router import news_router
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(stock_calculator, tags=['Calculators'])
app.include_router(AI_router, tags=['AI'])
app.include_router(company_router, tags=['Company'])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
