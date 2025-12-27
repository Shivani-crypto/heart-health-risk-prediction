import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re
import sqlite3
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import joblib


# Flask app setup
app = Flask(__name__)
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        age = int(request.form["age"])
        trestbps = int(request.form["trestbps"])
        chol = int(request.form["chol"])
        thalach = int(request.form["thalach"])

        data = np.array([[age, trestbps, chol, thalach]])
        data = scaler.transform(data)

        prediction = model.predict(data)[0]

        result = "High Risk" if prediction == 1 else "Low Risk"

        return render_template("result.html", result=result)

    return render_template("home.html")   


# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "GET":
#         return render_template("signup.html")
#     else:
#         username = request.form.get('user','')
#         name = request.form.get('name','')
#         email = request.form.get('email','')
#         number = request.form.get('mobile','')
#         password = request.form.get('password','')

#         # Server-side validation
#         username_pattern = r'^.{6,}$'
#         name_pattern = r'^[A-Za-z ]{3,}$'
#         email_pattern = r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$'
#         mobile_pattern = r'^[6-9][0-9]{9}$'
#         password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'

#         if not re.match(username_pattern, username):
#             return render_template("signup.html", message="Username must be at least 6 characters.")
#         if not re.match(name_pattern, name):
#             return render_template("signup.html", message="Full Name must be at least 3 letters, only letters and spaces allowed.")
#         if not re.match(email_pattern, email):
#             return render_template("signup.html", message="Enter a valid email address.")
#         if not re.match(mobile_pattern, number):
#             return render_template("signup.html", message="Mobile must start with 6-9 and be 10 digits.")
#         if not re.match(password_pattern, password):
#             return render_template("signup.html", message="Password must be at least 8 characters, with an uppercase letter, a number, and a lowercase letter.")

#         con = sqlite3.connect('signup.db')
#         cur = con.cursor()
#         cur.execute("SELECT 1 FROM info WHERE user = ?", (username,))
#         if cur.fetchone():
#             con.close()
#             return render_template("signup.html", message="Username already exists. Please choose another.")
        
#         cur.execute("insert into `info` (`user`,`name`, `email`,`mobile`,`password`) VALUES (?, ?, ?, ?, ?)",(username,name,email,number,password))
#         con.commit()
#         con.close()
#         return redirect(url_for('login'))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        mail1 = request.form.get('user','')
        password1 = request.form.get('password','')
        # con = sqlite3.connect('signup.db')
        # cur = con.cursor()
        # cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))

        if mail1 == 'admin' and password1 == 'admin':
            return render_template("home.html")
        else:
            return render_template("signin.html", message="Invalid username or password.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('signin.html')

# @app.route('/logon')
# def logon():
#     return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/graphs")
def about1():
    return render_template("graphs.html")

@app.route("/Notebook")
def about2():
    return render_template("Notebook.html")


   
if __name__ == '__main__':
    app.run()