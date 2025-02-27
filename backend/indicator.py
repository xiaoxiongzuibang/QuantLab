import talib as ta
import pandas as pd

def compute_sma(data: pd.Series, time: int = 20):
    sma = ta.SMA(data.values, timeperiod = time)
    return sma

def compute_ema(data: pd.Series, time: int = 20):
    ema = ta.EMA(data.values, timeperiod = time)
    return ema

def compute_macd(data: pd.Series, time: int = 20):
    macd = ta.MACD(data.values, timeperiod = time)
    return macd

