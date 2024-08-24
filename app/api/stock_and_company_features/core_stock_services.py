from app.data.requests.stock_fetches import  fetch_stock_months_av
import matplotlib.pyplot as plt
import pandas as pd
import io


def monthly_visualisation(symbol):
    try:
        data = fetch_stock_months_av(symbol)
        info = pd.DataFrame(data['Monthly Time Series']).transpose()
        info.index = pd.to_datetime(info.index)
        dates = info.index
        close = info['4. close'].astype(float).values

        plt.figure(figsize=(10, 5))
        plt.plot(dates, close, marker='o', linestyle='-', color='b')
        plt.title(f'Monthly Close Prices for {symbol}')
        plt.xlabel('Month')
        plt.ylabel('Close Price')
        plt.grid(True)

        plt.text(dates[0], close[0], f'Start: {dates[0].strftime("%Y-%m-%d")}', ha='right', fontsize=10, color='green')
        plt.text(dates[-1], close[-1], f'End: {dates[-1].strftime("%Y-%m-%d")}', ha='left', fontsize=10, color='red')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf
    except Exception as e:
        return f"Error related to monthly stock performance visualisation"