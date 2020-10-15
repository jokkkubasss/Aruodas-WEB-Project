from flask import Flask, render_template, request, jsonify
from model import Model

app = Flask(__name__)

my_model = Model()
my_model.train_model()

@app.route('/', methods=["GET", "POST"])
def index():
    #get info for selects
    return render_template('home.html')


@app.route('/estimation', methods=["GET", "POST"])
def estimation():
    if request.method == 'POST':
        est = my_model.predict(request.form)
        return render_template('estimation.html', est="€{:,.2f}".format(est[0]))

    return render_template('estimation.html')


@app.route('/get_address', methods=["POST"])
def get_address():
    if request.method == 'POST':
        print(request.form['long'])
        return jsonify({"data" : {"address":"18 \u0160vitrigailos gatv\u0117, LT-03011 Vilnius, Lithuania"}})


app.run('127.0.0.1', debug=True)