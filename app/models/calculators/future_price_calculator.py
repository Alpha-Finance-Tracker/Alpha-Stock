from app.models.base_models.stock_calculator import StockCalculator
from app.models.data_stream.alpha_vantage_data import AlphaVantage
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class StockPredictor(StockCalculator):

    def __init__(self,symbol):
        self.symbol = symbol
        self.alpha_vantage = AlphaVantage(self.symbol)


    def calculate(self):
        data = self.alpha_vantage.stock_monthly_adjusted()
        try:
            open = data.loc['1. open', :].values.astype(float)
            high = data.loc['2. high', :].values.astype(float)
            low = data.loc['3. low', :].values.astype(float)
            close = data.loc['4. close', :].values.astype(float)
            adjusted_close = data.loc['5. adjusted close', :].values.astype(float)
            volume = data.loc['6. volume', :].values.astype(float)
            dividend = data.loc['7. dividend amount', :].values.astype(float)

            x = np.array([open, high, low, close, adjusted_close, volume, dividend])
            x = x.T
            y = close

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            model = LinearRegression()
            model.fit(x_train, y_train)

            y_pred = model.predict(x_test)

            mse = mean_squared_error(y_test, y_pred)
            root_mean_square_deviation = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)

            avg_predicted_price = np.mean(y_pred)

            return {'average_predicted_price':avg_predicted_price,
                      'The root mean square deviation': root_mean_square_deviation,
                      'The r2': r2}

        except Exception as e:
            return f'Error with the data {e}'
