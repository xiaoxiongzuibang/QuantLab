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
    image_data = None
    if request.method == 'POST':
        ticker = request.form.get('stock')
        start = request.form.get('start')
        end = request.form.get('end')
        if ticker and start and end:
            data = get_stock_data(ticker, start, end)
            image_data = plot_stock_data(data)
    return render_template("workspace.html", image_data = image_data)

if __name__ == "__main__":
    app.run(debug = True)