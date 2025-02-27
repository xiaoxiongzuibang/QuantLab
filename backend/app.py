from flask import Flask, render_template, request
from data import *
from strategy import *

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/backtest", methods = ['GET', 'POST'])
def backtest():
    ticker = None
    start = None
    end = None
    strategy = None
    image_data = None
    transaction = None
    ar = None
    s_ar = None
    outperformance = None
    vol = None
    # beta = None
    if request.method == 'POST':
        '''Request data from frontend'''
        ticker = request.form.get('stock')
        start = request.form.get('start')
        end = request.form.get('end')
        strategy = request.form.get('strategy')

        '''Load Data Class'''
        data = Data(ticker, start, end)
        stock_data = data.get_stock_data()
        ar = data.get_ar()
        vol = data.get_volatility()
        image_data = plot_stock_data(stock_data)

        '''Strategy Selection'''
        if strategy == "Long":
            strategy = LongStrategy(stock_data)
            s_ar = strategy.get_ar()
            outperformance = s_ar - ar
            transaction = strategy.get_transaction()

    return render_template("backtest.html", ticker = ticker, start = start, end = end, 
                           image_data = image_data, ar = ar, vol = vol, outperformance = outperformance, 
                           transaction = transaction
                           )

if __name__ == "__main__":
    app.run(debug = True)