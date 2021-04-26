from flask import Flask, render_template, redirect, url_for, request

import pickle
import numpy
import pandas
from matplotlib import pyplot
import seaborn
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import ipywidgets
import warnings
warnings.filterwarnings('ignore')

# load model

svc = pickle.load(open('svc.pkl.pkl','rb'))

app = Flask(__name__)


@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")


# @app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        fixed_acidity = request.form['fixed_acidity']
        volatile_acidity = request.form['volatile_acidity']
        citric_acid = request.form['citric_acid']
        residual_sugar = request.form['residual_sugar']
        chlorides = request.form['chlorides']
        free_sulfur_dioxide = request.form['free_sulfur_dioxide']
        total_sulfur_dioxide = request.form['total_sulfur_dioxide']
        density = request.form['density']
        ph = request.form['ph']
        sulphates = request.form['sulphates']
        alcohol = request.form['alcohol']
        prediction = predict(fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol)
    else:
        return render_template("web.html")

    return render_template("web.html", prediction=prediction, facid=fixed_acidity, vacid=volatile_acidity,
                           cacid=citric_acid, rs=residual_sugar, ch=chlorides, fsd=free_sulfur_dioxide,
                           tsd=total_sulfur_dioxide, den=density, ph=ph, sul=sulphates, alc=alcohol)


@app.route('/logout')
def logout():
    return redirect(url_for("login"))


@app.route('/submit', methods=['POST'])
def submit():
    user = "test"
    pswd = "test"
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if (username == user) and (password == pswd):
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))


def predict(facid, vacid, cacid, rs, ch, fsd, tsd, den, ph, sul, alc):
    user_data = [facid, vacid, cacid, rs, ch, fsd, tsd, den, ph, sul, alc]
    user_data_asarray = numpy.asarray(user_data)
    reshaped_data = user_data_asarray.reshape(1, -1)
    prediction = svc.predict(reshaped_data)
    if prediction[0] == 0:
        return ("Poor Quality Wine")
    else:
        return ("High Quality Wine")


if __name__ == "__main__":
    app.run()

