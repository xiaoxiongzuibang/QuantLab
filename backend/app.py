from flask import Flask, render_template, request
from data import get_stock_data, plot_stock_data

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crashcourse")
def crashcourse():
    return render_template("crashcourse.html")

@app.route("/workspace", methods = ['GET', 'POST'])
def workspace():
    ticker = None
    start = None
    end = None
    image_data = None
    rate_of_return = None
    if request.method == 'POST':
        ticker = request.form.get('stock')
        start = request.form.get('start')
        end = request.form.get('end')
        if ticker and start and end:
            data = get_stock_data(ticker, start, end)
            image_data = plot_stock_data(data)
            rate_of_return = round(((data.iloc[-1]['Close'] - data.iloc[0]['Close'])/data.iloc[0]['Close'])*100,2).item()
    return render_template("workspace.html", image_data = image_data, ticker = ticker, rate_of_return = rate_of_return, start = start, end = end)

if __name__ == "__main__":
    app.run(debug = True)