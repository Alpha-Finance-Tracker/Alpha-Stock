import yfinance as yf
import pandas as pd

from app.api.AI_features.open_ai_services import fetch_competitors


class YahooFinance:

    def fetch_cash_flow(self, symbol):
        ticker = yf.Ticker(symbol)
        cash_flow = ticker.cash_flow.infer_objects(copy=False).fillna(0)
        return pd.DataFrame(cash_flow)

    def fetch_market_data(self, symbol):
        market_data = yf.download(f'{symbol}')
        return market_data

    def fetch_company_pe_ratio(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            pe_ratio = stock.info['forwardPE']
            return float(pe_ratio)
        except Exception as e:
            print(f"Error fetching P/E ratio for {symbol}: {e}")
            return None

    def fetch_company_beta(self, symbol):
        stock_data = yf.Ticker(symbol)
        historical_data = stock_data.history(period="max")
        beta = historical_data['Close'].pct_change().cov(historical_data['Close'].pct_change())
        return beta

    def fetch_competitors_eps(self, symbol, sector):
        competitors = fetch_competitors(symbol, sector)
        competitors_pe_ratio = []

        for x in competitors:
            eps = self.fetch_company_pe_ratio(x)
            if eps:
                competitors_pe_ratio.append(eps)

        return competitors_pe_ratio
