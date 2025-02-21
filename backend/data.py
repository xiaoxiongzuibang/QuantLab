import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import datetime
import base64
import io

def get_stock_data(ticker, time_range):
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days = int(time_range))
    data = yf.download(ticker, start = start_date, end = end_date)
    return data


def plot_stock_data(data):
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.title('Stock Price Chart')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.getvalue()).decode('utf8')
    print(len(image_data))
    plt.close()
    return image_data
