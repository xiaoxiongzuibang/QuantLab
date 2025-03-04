from flask import Flask, render_template, request
from data import *
from strategy import *

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/backtest", methods = ['GET', 'POST'])
def backtest():
    '''获取HTML前端输入变量'''
    context = {}
    context['ticker'] = request.form.get('Stock')
    context['amount'] = request.form.get('Amount')
    context['start'] = request.form.get('Start')
    context['end'] = request.form.get('End')
    context['strategy'] = request.form.get('Strategy')

    '''Load Data Class'''
    data = Data(ticker, start, end)
    stock_data = data.get_stock_data()
    ar = data.get_ar()
    vol = data.get_volatility()
    image_data = plot_stock_data(stock_data)

    '''Strategy Selection'''
    if strategy == "dsma":
        strategy = DSMAStrategy(stock_data)
        s_ar = strategy.get_ar()
        outperformance = s_ar - ar
        transaction = strategy.get_transaction()

    return render_template("backtest.html", **context)

if __name__ == "__main__":
    app.run(debug = True)