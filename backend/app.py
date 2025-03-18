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

@app.route("/crashcourse")
def crashcourse():
    return render_template("crashcourse.html")

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

        context['strategy'] = request.form.get('Strategy')

        '''DSMA and DEMA Strategy: for one particular stock'''
        if context['strategy'] == 'dsma' or context['strategy'] == 'dema':
            strategy_dic = {
                'dsma': DSMAStrategy,
                'dema': DEMAStrategy
            }

            '''Load Data Class'''
            context['ticker'] = request.form.get('Ticker')
            context['amount'] = request.form.get('Amount')
            context['riskfreerate'] = float(request.form.get('RiskFreeRate'))
            context['start'] = request.form.get('Start')
            context['end'] = request.form.get('End')
            context['duration'] = duration_days
            dataframe = yf.download(context['ticker'], start = context['start'], end = context['end'])
            start_price, end_price = dataframe['Close'].iloc[0], dataframe['Close'].iloc[-1]
            cagr = (end_price / start_price)**(252.0/duration_days) - 1
            context['cagr'] = cagr.values[0]

            dataframe.columns = dataframe.columns.get_level_values(0)
            dataframe.columns = [col.lower() for col in dataframe.columns]

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
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=context['riskfreerate'], annualize=True, _name='SharpeRatio')

            '''Start cerebro'''
            results = cerebro.run()
            result = results[0]

            '''Compute Annualized Return'''
            annual_return = result.analyzers.AnnualReturn.get_analysis()
            annualized_return = next(iter(annual_return.values()))
            context['annualized_return'] = round(annualized_return, 4)

            '''Compute Sharpe Ratio'''
            sharpe_ratio = result.analyzers.SharpeRatio.get_analysis()
            sharpe_ratio = next(iter(sharpe_ratio.values()))
            context['sharpe_ratio'] = round(sharpe_ratio, 4)

            figs = cerebro.plot(volume=False)
            fig = figs[0][0]
            buf = io.BytesIO()
            fig.set_size_inches(20, 12)
            fig.savefig(buf, format='png', dpi=300)
            buf.seek(0)
            img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
            
            return render_template("backtest.html", image_data=img_data, **context)
    
        if context['strategy'] == 'pair':

            '''Load Data Class'''
            context['ticker1'] = request.form.get('Ticker1')
            context['ticker2'] = request.form.get('Ticker2')
            context['amount'] = request.form.get('Amount')
            context['riskfreerate'] = float(request.form.get('RiskFreeRate'))
            context['start'] = request.form.get('Start')
            context['end'] = request.form.get('End')
            context['duration'] = duration_days
            dataframe1 = yf.download(context['ticker1'], start = context['start'], end = context['end'])
            dataframe2 = yf.download(context['ticker2'], start = context['start'], end = context['end'])
            print(dataframe1.shape)
            print(dataframe2.shape)
            start_price1, end_price1 = dataframe1['Close'].iloc[0], dataframe1['Close'].iloc[-1]
            start_price2, end_price2 = dataframe2['Close'].iloc[0], dataframe2['Close'].iloc[-1]
            cagr1 = (end_price1 / start_price1)**(252.0/duration_days) - 1
            cagr2 = (end_price2 / start_price2)**(252.0/duration_days) - 1
            context['cagr1'] = cagr1.values[0]
            context['cagr2'] = cagr2.values[0]

            dataframe1.columns = dataframe1.columns.get_level_values(0)
            dataframe1.columns = [col.lower() for col in dataframe1.columns]

            dataframe2.columns = dataframe2.columns.get_level_values(0)
            dataframe2.columns = [col.lower() for col in dataframe2.columns]

            '''Load Cerebro'''
            cerebro =  MyCerebro()
            data1 = bt.feeds.PandasData(dataname = dataframe1, timeframe = bt.TimeFrame.Days)
            data2 = bt.feeds.PandasData(dataname = dataframe2, timeframe = bt.TimeFrame.Days)
            cerebro.adddata(data1)
            cerebro.adddata(data2)
            cerebro.addstrategy(PAIRStrategy)
            cerebro.broker.setcash(10000.0)
            cerebro.broker.setcommission(commission = 0.0005)
            cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)

            '''Add Analyzers'''
            cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=context['riskfreerate'], annualize=True, _name='SharpeRatio')

            '''Start cerebro'''
            results = cerebro.run()
            result = results[0]

            '''Compute Annualized Return'''
            annual_return = result.analyzers.AnnualReturn.get_analysis()
            annualized_return = next(iter(annual_return.values()))
            context['annualized_return'] = round(annualized_return, 4)

            '''Compute Sharpe Ratio'''
            sharpe_ratio = result.analyzers.SharpeRatio.get_analysis()
            sharpe_ratio = next(iter(sharpe_ratio.values()))
            context['sharpe_ratio'] = round(sharpe_ratio, 4)

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