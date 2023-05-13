import os
from datetime import timedelta, datetime
from flask import Flask, redirect, render_template, request, session,redirect, url_for
from werkzeug.urls import url_encode
import pandas as pd
import joblib
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "hellothere"
app.permanent_session_lifetime = timedelta(minutes = 15)
name = ""
#App routes:
#Home
@app.route("/home")
@app.route("/")
def front():
    return render_template("index.html")

#Submit first form
@app.route("/result", methods = ["GET", "POST"])
def result():
    if request.method == 'POST' or request.method == 'GET':
        pipe = joblib.load('assets/model/decision_tree.sav')
        sheet_id = "1tEGHGwusxsX1Muw4haUhTMtZnNC7AcXhvzbUo_Q5boo"
        sheet_name = "Form Responses 2"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        url = url.replace(" ", "%20")
        X = pd.read_csv(url)
        X = X.rename(columns={'Enter Your Name': 'pname', 'Email Address' : 'BMI', 'Enter your body weight (in kg)':'Weight', 'Enter your height (in cm)' : 'Height', 'Enter Your Age' : 'Age', 'Do you Smoke' : 'Smoke', 'Do you consume alcohol?' : 'Alcohol', 'Have you ever had a heart attack or stroke?' : 'Stroke', 'From how many days have you been experiencing weak physical health?' : 'PhysicalHealth', 'From how many days have you been experiencing weak mental health?' : 'MentalHealth', 'Do you have difficulty in walking?' : 'DiffWalking', 'Do you have diabetes?' : 'Diabetic', 'Do you do any physical activity other than work?' : 'PhysicalAct', 'How many hours of sleep do you typically get per night?' : 'Sleep', 'Do you have Asthama?': 'Asthama', 'Do you have kidney disease?"' : 'Kidney'})
   
        X =  X[X.columns].replace({'Yes':1, 'No':0, 'Male':1, "Female":0 })
        X.BMI = X.Weight / (X.Height * X.Height / 10000)
        n = X.pname.iloc[-1]
        global name  
        name = n
        X = X.drop(['Timestamp', 'pname','Weight', 'Height'], axis=1)
        transformer = make_column_transformer((OneHotEncoder(sparse=False), ['Age']), remainder='passthrough')

        # Encode test data 
        transformed_test = transformer.fit_transform(X)
        transformed_test_data = pd.DataFrame(transformed_test, columns=transformer.get_feature_names())

        # Concat the two tables
        transformed_test_data.reset_index(drop=True, inplace=True)
        X.reset_index(drop=True, inplace=True)
        X = transformed_test_data
        
        scaler = MinMaxScaler(feature_range=(-1,1)).fit(X)
        
        # Scale test data
        X = scaler.fit_transform(X)
        res = X[[-1]]
        # apply the whole pipeline to data
        pred = pipe.predict(X[[-1]])
        return render_template("result.html", predict=pred, result = n)
    return redirect("/")
   
   
@app.route("/advanced", methods = ["GET", "POST"])
def advanced():
    if request.method == 'POST' or request.method == 'GET':
        pipetree = joblib.load('assets/model/decision_treeDet.sav')
        pipeKNN = joblib.load('assets/model/KNNDet.sav')
        sheet_id = "17f2EVE10PNwfjAqZHgcv86qTz15xA2SeNgKaHHCrzoo"
        sheet_name = "Form Responses 1"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        url = url.replace(" ", "%20")
        X = pd.read_csv(url)
        X = X.rename(columns={'Enter Your Age ': 'Age', 'Chest Pain Type' : 'ChestPain', 'Blood Pressure (in mm Hg)':'BP', 'Cholestrol (in mg/dl)' : 'Cholesterol', 'Fasting Blood Sugar (FBS)' : 'FBS120', 'Resting Electrocardiogram result' : 'RES', 'Maximum Heart Rate ' : 'MaxHeart', 'Exercise Angina' : 'ExerAngina', ' ST depression induced by exercise compared to rest' : 'STDepression', 'Slope of ST' : 'SlopeST', 'Number of Vessels Fluro' : 'NumVesselFluro', 'Thallium ':'Thallium'})
        X = X[X.columns].replace({'Yes':1, 'No':0, 'Male':1, 'Female':0, 'Other':1, 'Typical Agina':1, 'Atypical Agina':2, 'Non-Anginal Pain': 3, 'Asymptomatic': 4, 'Normal': 0, 'Having ST - T wave abnormally': 1, 'Showing probable': 2, 'Unsloping': 1, 'Flat': 2, 'Downsloping': 3, '3 : Normal' : 3, '6 : Fixed Defect': 6, '7 : Reversable Defect': 7, '0': 1, '1':1, '2':2, '3':3})
        X = X.drop(['Timestamp'], axis=1)  
        transformer = make_column_transformer((OneHotEncoder(sparse=False), ['ChestPain', 'RES', 'SlopeST', 'NumVesselFluro', 'Thallium']), remainder='passthrough')

        # Encode test data 
        transformed_test = transformer.fit_transform(X)
        transformed_test_data = pd.DataFrame(transformed_test, columns=transformer.get_feature_names())

        # Concat the two tables
        transformed_test_data.reset_index(drop=True, inplace=True)
        X.reset_index(drop=True, inplace=True)
        X = transformed_test_data
                
        scaler = MinMaxScaler(feature_range=(-1,1)).fit(X)
                
        # Scale test data
        X = scaler.fit_transform(X)
        # apply the whole pipeline to data
        pred1 = pipetree.predict(X[[-1]])
        pred2 = pipeKNN.predict(X[[-1]])
        
        return render_template("advanced.html", pred1 = pred1, pred2 = pred2, name=name)
    return redirect("/")
    
#Run the app
if __name__ == "__app__":
    app.run(debug=True, port=8098)

app.run(port=8098)