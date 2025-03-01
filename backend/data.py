import yfinance as yf
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import base64
import io

class Data:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end

    def get_stock_data(self):
        '''由于前端datetime-local数据和这里接受的数据不太一样 因此如果使用
        则需要使用datetime.datetime.formisoformat()来处理数据'''
        # start = datetime.datetime.fromisoformat(start)
        # end = datetime.datetime.fromisoformat(end)
        data = yf.download(self.ticker, start = self.start, end = self.end)
        return data
    
    def get_exchange(self):
        ticker_obj = yf.Ticker(self.ticker)
        info = ticker_obj.info
        return info.get('exchange')
    
    # Calculate Holding Periode Return
    def get_hpr(self):
        hpr = round((((self.data.iloc[-1]['Close'] - self.data.iloc[0]['Close']) / self.data.iloc[0]['Close']) * 100).item(), 2)
        return hpr
    
    # Calculate Annualized Return
    def get_ar(self):
        hpr = round((((self.data.iloc[-1]['Close'] - self.data.iloc[0]['Close']) / self.data.iloc[0]['Close']) * 100).item(), 2)
        ar = hpr * 365 / datetime.timedelta(self.start, self.end)
        return ar
    
    # Calculate Volatility
    def get_volatility(self):
        vol = np.var(self.data.loc['Close'])
        return vol
    
    # Calculate Beta
    def get_beta(self, benchmark_data):
        beta = np.cov(self.data.iloc['Close'], benchmark_data.iloc['Close'])
        return beta
    
    # Calculate Sharp Ratio
    def get_sharp_ration(self, benchmark_data, ar, rf, volatility):
        sharp_ratio = ((ar - rf) / volatility) * 100
        return sharp_ratio


def plot_stock_data(data):
    plt.figure(figsize=(10,5))
    plt.title('Stock Price Chart')
    plt.plot(data.index, data['Close'], label='Close Price')
    # plot benchmark figure
    # plt.plot(data.index, data['Close'], label='S&P 500')
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