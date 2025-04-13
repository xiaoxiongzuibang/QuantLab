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

class PAIRIndicators(bt.Indicator):
    params = (
        ('period', 20),
    )
    lines = ('spread', 'spread_mean', 'spread_std', 'zscore',)
    def __init__(self):
        self.lines.spread = self.datas[0] - self.datas[1]
        self.lines.spread_mean = bt.indicators.SimpleMovingAverage(self.lines.spread, period = self.p.period)
        self.lines.spread_std = bt.indicators.StandardDeviation(self.lines.spread, period = self.p.period)
        self.lines.zscore = (self.lines.spread - self.lines.spread_mean) / (self.lines.spread_std + 1e-7)

class PAIRStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('signal', 2),
        ('size', 10),
        ('revert_signal', 0.05),
    )

    def __init__(self):
        self.pair_indicators = PAIRIndicators(
            self.datas[0], self.datas[1],
            period=self.p.period
        )

    def next(self):
        zscore = self.pair_indicators.zscore[0]
        position1 = self.getposition(self.datas[0]).size
        position2 = self.getposition(self.datas[1]).size

        if position1 == 0 and position2 == 0:
            if -self.p.signal< zscore < self.p.signal:
                pass
            elif zscore > self.p.signal:
                self.sell(data = self.datas[0], size = self.p.size)
                self.buy(data = self.datas[1], size = self.p.size)
            elif zscore < -self.p.signal:
                self.sell(data = self.datas[1], size = self.p.size)
                self.buy(data = self.datas[0], size = self.p.size)
        elif position1 != 0 and position2 != 0:
            if zscore > self.p.revert_signal or zscore < -self.p.revert_signal:
                pass
            if  abs(zscore) < self.p.revert_signal:
                self.close(self.datas[0])
                self.close(self.datas[1])

        # current_bar_index = len(self.data0)
        # total_bars = self.data0.buflen()
        # if current_bar_index >= (total_bars - 1):
        #     self.close(self.datas[0])
        #     self.close(self.datas[1])