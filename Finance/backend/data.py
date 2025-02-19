import tushare as ts
import matplotlib.pyplot as plt

ts.set_token("09168084438f7ab814f193d074fc1883fcab62fede31c4b2f988290e")

pro = ts.pro_api()
df = pro.daily(ts_code='600519.SH', start_date='20230101', end_date='20231231')
print(df.head())

plt.figure(figsize=(16, 6))
plt.plot(df['trade_date'], df['close'])
plt.show()