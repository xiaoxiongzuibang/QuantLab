from data import *
import pandas as pd
from indicator import *
import backtrader as bt
from abc import ABC, abstractmethod

# class Strategy(ABC):
#     '''
#     Each strategy have its own logic, but there are some methodes that they have to reach.
#     Create an abstract base class Strategy(ABC)
#     '''
#     def __init__(self, data: pd.DataFrame, **kwargs): 
#         self.data = data.copy()
#         self.params = kwargs

#     @abstractmethod
#     def transaction_signal(self) -> pd.DataFrame:
#         '''Each strategy must generate trasaction signals'''
#         pass

#     @abstractmethod
#     def backtest(self) -> dict:
#         '''Each strategy must have backtest function to get result'''
#         pass

# class LongStrategy(Strategy):
#     def transaction_signal(self) -> pd.DataFrame:
#         '''
#         This is a simple long.
#         '''
#         self.data['Signal'] = 0
#         self.data.loc[self.data['Close']>self.data['SMA]'], 'Signal'] = 1
#         self.data['Position'] = self.data['Signal'].diff()
#         return self.data
    
#     def backtest(self):
#         dict = {
#             'hpr': hpr,
#             'ar': ar,
#             'outperformance': outperformance,
#             'beta': beta
#         }
#         return dict

# class SMAStrategy(Strategy):
#     def transaction_signal(self) -> pd.DataFrame:
#         '''
#         Use talib to compute SMA, the signal reflact only the market state
#         We use the difference of signal to decide position 
#         '''
#         self.data['SMA'] = compute_sma(self.data['Close'], 20)
#         self.data['Signal'] = 0
#         self.data.loc[self.data['Close']>self.data['SMA]'], 'Signal'] = 1
#         self.data['Position'] = self.data['Signal'].diff()
#         return self.data
    
#     def backtest(self):
#         dict = {
#             'hpr': hpr,
#             'ar': ar,
#             'outperformance': outperformance,
#             'beta': beta
#         }
#         return dict


# def ShortStrategy(data):
#     rate_of_return = -1 * round((((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100).item(), 2)
#     return rate_of_return

# class MovingAverageStrategy:
#     def __init__(self, data):
#         self.data = data

# strategy.py

class DoubleMAStrategy(bt.Strategy):
    """
    双均线策略示例：
    - 当快均线 > 慢均线时买入
    - 当快均线 < 慢均线时卖出
    """

    # 定义策略可调参数
    params = (
        ("fast_period", 10),  # 快均线周期
        ("slow_period", 30),  # 慢均线周期
    )

    def __init__(self):
        """
        初始化策略时自动调用：
        1. 定义/获取指标
        2. 准备策略需要的变量
        """
        # 定义快均线（SMA）
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.p.fast_period
        )
        # 定义慢均线（SMA）
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.p.slow_period
        )

    def next(self):
        """
        每根bar到来时会被调用一次：
        1. 检查快慢均线关系
        2. 根据是否持仓决定买卖操作
        """
        # 如果当前没有持仓
        if not self.position:
            # 如果快均线穿越慢均线 => 买入
            if self.fast_ma[0] > self.slow_ma[0]:
                self.buy()
        else:
            # 如果已经持仓，当快均线 < 慢均线 => 卖出
            if self.fast_ma[0] < self.slow_ma[0]:
                self.close()  # 平掉当前持仓