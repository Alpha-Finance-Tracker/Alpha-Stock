import yfinance as yf
import pandas as pd

class YahooFinance:

    def fetch_cash_flow(self, symbol):
        ticker = yf.Ticker(symbol)
        cash_flow = ticker.cash_flow.infer_objects(copy=False).fillna(0)
        return pd.DataFrame(cash_flow)

    def fetch_market_data(self, symbol):
        market_data = yf.download(f'{symbol}')
        return market_data

    def fetch_company_price_to_earnings_ratio(self, symbol):
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

    def growth_estimates(self,symbol):
        stock_data = yf.Ticker(symbol)
        return stock_data.growth_estimates.to_json
