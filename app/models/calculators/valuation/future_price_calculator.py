from app.models.base_models.stock_calculator import StockCalculator
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from app.models.data_stream.yahoo_finance_data import YahooFinance


class StockPredictor(StockCalculator):

    def __init__(self, symbol):
        self.symbol = symbol
        self.yahoo_finance = YahooFinance(self.symbol)

    async def calculate(self):
        try:

            data = await self.yahoo_finance.market_data()
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_columns):
                raise ValueError("Data missing required columns")

            monthly_data = data.resample('M').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            })

            features = ['Open', 'High', 'Low', 'Close', 'Volume']
            X = monthly_data[features].values
            y = monthly_data['Close'].values

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Predict and evaluate
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            root_mean_square_deviation = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            avg_predicted_price = np.mean(y_pred)

            return {
                'average_predicted_price': avg_predicted_price,
                'root_mean_square_deviation': root_mean_square_deviation,
                'r2': r2
            }

        except Exception as e:
            return f'Error with the data {e}'
