import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def stock_predictor(data):
    try:
        open = data.loc['1. open', :].values.astype(float)
        high = data.loc['2. high', :].values.astype(float)
        low = data.loc['3. low', :].values.astype(float)
        close = data.loc['4. close', :].values.astype(float)
        adjusted_close = data.loc['5. adjusted close', :].values.astype(float)
        volume = data.loc['6. volume', :].values.astype(float)
        dividend = data.loc['7. dividend amount', :].values.astype(float)


        x = np.array([open, high, low, close, adjusted_close, volume, dividend])
        x = x.T  # Transpose x to have (296, 7)
        y = close


        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

        model = LinearRegression()
        model.fit(x_train,y_train)

        y_pred = model.predict(x_test)

        mse = mean_squared_error(y_test,y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        p_df = pd.DataFrame(y_test,y_pred)

        avg_predicted_price = np.mean(y_pred)

        return f'The avg predicted price {avg_predicted_price}, ' \
               f'The rmse {rmse}, ' \
               f'The r2 {r2}'
    except Exception as e:
        return f'Error with the data {e}'

