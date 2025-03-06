import matplotlib
matplotlib.use('Agg')
import io
import base64
import matplotlib.pyplot as plt
import backtrader as bt
from mycerebro import MyCerebro
import yfinance as yf
import datetime
from flask import Flask, render_template, request
from data import *
from strategy import *

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/backtest", methods = ['GET', 'POST'])
def backtest():
    context = {}
    if request.method == "POST":
        '''获取HTML前端输入变量'''
        start_str = request.form.get('Start')
        end_str = request.form.get('End')

        fmt = '%Y-%m-%d'
        start_dt = datetime.datetime.strptime(start_str, fmt).date()
        end_dt = datetime.datetime.strptime(end_str, fmt).date()
        duration_days = (end_dt - start_dt).days

        context['ticker'] = request.form.get('Ticker')
        context['amount'] = request.form.get('Amount')
        context['start'] = request.form.get('Start')
        context['end'] = request.form.get('End')
        context['duration'] = duration_days
        context['strategy'] = request.form.get('Strategy')

        '''Load Data Class'''
        dataframe = yf.download(context['ticker'], start = context['start'], end = context['end'])
        dataframe.columns = dataframe.columns.get_level_values(0)
        dataframe.columns = [col.lower() for col in dataframe.columns]

        '''Strategy Selection'''
        strategy_dic = {
            'dsma': DSMAStrategy,
            'dema': DEMAStrategy
        }

        '''Load Cerebro'''
        cerebro =  MyCerebro()
        data = bt.feeds.PandasData(dataname = dataframe, timeframe = bt.TimeFrame.Days)
        cerebro.adddata(data)
        cerebro.addstrategy(strategy_dic[context['strategy']])
        cerebro.broker.setcash(10000.0)
        cerebro.broker.setcommission(commission = 0.0005)
        cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)

        '''Add Analyzers'''
        cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.02, annualize=True, _name='SharpeRatio')

        '''Start cerebro'''
        results = cerebro.run()
        result = results[0]

        '''Compute Annualized Return'''
        annual_return = result.analyzers.AnnualReturn.get_analysis()
        sannual_return = next(iter(annual_return.values()))
        context['annual_return'] = f"{round(sannual_return, 2)*100}%"

        '''Compute Sharpe Ratio'''
        sharpe_ratio = result.analyzers.SharpeRatio.get_analysis()
        ssharpe_ratio = next(iter(sharpe_ratio.values()))
        context['sharpe_ratio'] = round(ssharpe_ratio, 2)

        

        figs = cerebro.plot(volume=False)
        fig = figs[0][0]
        buf = io.BytesIO()
        fig.set_size_inches(20, 12)
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
        
        return render_template("backtest.html", image_data=img_data, **context)
    
    else:
        return render_template("backtest.html")

if __name__ == "__main__":
    app.run(debug = True)