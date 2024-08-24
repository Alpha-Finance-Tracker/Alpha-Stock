from app.api.AI_features.stock_predictor import stock_predictor
from app.data.requests.stock_fetches import fetch_stock_monthly_adjusted_av
import pandas as pd


def ml_stock_prediction(stock):
    data = fetch_stock_monthly_adjusted_av(stock)
    info = pd.DataFrame(data['Monthly Adjusted Time Series'])
    return stock_predictor(info)
