import yfinance as yf
import pandas as pd
import backtrader as bt
import datetime

class DSMAStrategy(bt.Strategy):
    def __init__(self):
        # self.data = self.datas0.close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.fast_sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = 5)
        self.slow_sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = 20)

    def next(self):
        if not self.position:
            if self.fast_sma > self.slow_sma:
                self.buy()
        else:
            if self.fast_sma < self.slow_sma:
                self.close()

class DEMAStrategy(bt.Strategy):
    def __init__(self):
        # self.data = self.datas0.close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.fast_ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period = 5)
        self.slow_ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period = 20)

    def next(self):
        if not self.position:
            if self.fast_ema > self.slow_ema:
                self.buy()
        else:
            if self.fast_ema < self.slow_ema:
                self.close()

dataframe = yf.download('NVDA', start = '2022-07-03', end = '2025-02-03', group_by = 'column')
dataframe.columns = dataframe.columns.get_level_values(0)
# dataframe['Datetime'] = pd.to_datetime(dataframe['Date'])
# dataframe.set_index('Datetime', inplace = True)

print(dataframe.columns)
dataframe.columns = [col.lower() for col in dataframe.columns]

cerebro =  bt.Cerebro()
data = bt.feeds.PandasData(dataname = dataframe, fromdate = datetime.datetime(2022,7,3), todate = datetime.datetime(2025,2,3) , timeframe = bt.TimeFrame.Days)
cerebro.adddata(data)
cerebro.addstrategy(DEMAStrategy)

cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission = 0.0005)
cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)

result = cerebro.run()
cerebro.plot()