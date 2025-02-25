from flask import Flask, render_template, request
from data import get_stock_data, plot_stock_data
from strategy import *

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crashcourse")
def crashcourse():
    return render_template("crashcourse.html")

@app.route("/backtest", methods = ['GET', 'POST'])
def backtest():
    ticker = None
    start = None
    end = None
    strategy = None
    image_data = None
    transaction = None
    rate_of_return = None
    if request.method == 'POST':
        ticker = request.form.get('stock')
        start = request.form.get('start')
        end = request.form.get('end')
        strategy = request.form.get('strategy')
        if ticker and start and end:
            data = get_stock_data(ticker, start, end)
            image_data = plot_stock_data(data)
            if strategy == "Long":
                transaction = 2
                rate_of_return = LongStrategy(data)
    return render_template("backtest.html", image_data = image_data, ticker = ticker, transaction = transaction, rate_of_return = rate_of_return, start = start, end = end)

if __name__ == "__main__":
    app.run(debug = True)