import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import base64
import io

def get_stock_data(ticker, start, end):
    '''由于前端datetime-local数据和这里接受的数据不太一样 因此如果使用
    则需要使用datetime.datetime.formisoformat()来处理数据'''
    # start = datetime.datetime.fromisoformat(start)
    # end = datetime.datetime.fromisoformat(end)
    start = start
    end = end
    data = yf.download(ticker, start = start, end = end)
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