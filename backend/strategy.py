from data import *
import pandas as pd
from indicator import *
from abc import ABC, abstractmethod

class Strategy(ABC):
    '''
    Each strategy have its own logic, but there are some methodes that they have to reach.
    Create an abstract base class Strategy(ABC)
    '''
    def __init__(self, data: pd.DataFrame, **kwargs): 
        self.data = data.copy()
        self.params = kwargs

    @abstractmethod
    def transaction_signal(self) -> pd.DataFrame:
        '''Each strategy must generate trasaction signals'''
        pass

    @abstractmethod
    def backtest(self) -> dict:
        '''Each strategy must have backtest function to get result'''
        pass

class LongStrategy(Strategy):
    def transaction_signal(self) -> pd.DataFrame:
        '''
        This is a simple long.
        '''
        self.data['Signal'] = 0
        self.data.loc[self.data['Close']>self.data['SMA]'], 'Signal'] = 1
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def backtest(self):
        dict = {
            'hpr': hpr,
            'ar': ar,
            'outperformance': outperformance,
            'beta': beta
        }
        return dict

class SMAStrategy(Strategy):
    def transaction_signal(self) -> pd.DataFrame:
        '''
        Use talib to compute SMA, the signal reflact only the market state
        We use the difference of signal to decide position 
        '''
        self.data['SMA'] = compute_sma(self.data['Close'], 20)
        self.data['Signal'] = 0
        self.data.loc[self.data['Close']>self.data['SMA]'], 'Signal'] = 1
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def backtest(self):
        dict = {
            'hpr': hpr,
            'ar': ar,
            'outperformance': outperformance,
            'beta': beta
        }
        return dict


# def ShortStrategy(data):
#     rate_of_return = -1 * round((((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100).item(), 2)
#     return rate_of_return

# class MovingAverageStrategy:
#     def __init__(self, data):
#         self.data = data