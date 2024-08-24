import requests
from dotenv import dotenv_values

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
import pandas as pd


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
def fetch_news_from_alpha_vantage(stock:str):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    data_frame = pd.DataFrame(data['feed'])

    return data_frame