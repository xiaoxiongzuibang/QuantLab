from data import *
import pandas as pd
import backtrader as bt

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