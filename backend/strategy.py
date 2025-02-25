from data import *
import talib as ta

def LongStrategy(data):
    rate_of_return = round((((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100).item(), 2)
    return rate_of_return

def ShortStrategy(data):
    rate_of_return = -1 * round((((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100).item(), 2)
    return rate_of_return

# class MovingAverageStrategy:
#     def __init__(self, data):
#         self.data = data