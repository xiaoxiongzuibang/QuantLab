from data import *
import talib as ta
from abc import ABC, abstractmethod

class Strategy(ABS):
    def __init__(self, ticker):
        self.stock = Data(ticker)

    @abstractmethod

def LongStrategy(data):
    def __init__(self):

def ShortStrategy(data):
    rate_of_return = -1 * round((((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100).item(), 2)
    return rate_of_return

# class MovingAverageStrategy:
#     def __init__(self, data):
#         self.data = data