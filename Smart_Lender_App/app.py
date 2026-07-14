import pickle
from flask import Flask,render_template, request
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "models/loan_approval_model.pkl"
SCALER_PATH = "models/scaler.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)

#home route
@app.route("/")
def home():
    return render_template("index.html")

#form data recieved from the form
@app.route("/predict", methods=["POST"])
def predict():

    # Read form data
    gender = request.form["gender"]
    married = request.form["married"]
    dependents = request.form["dependents"]
    education = request.form["education"]
    self_employed = request.form["self_employed"]

    applicant_income = float(request.form["applicant_income"])
    coapplicant_income = float(request.form["coapplicant_income"])
    loan_amount = float(request.form["loan_amount"])
    loan_term = float(request.form["loan_term"])

    credit_history = float(request.form["credit_history"])
    property_area = request.form["property_area"]

    # ----------------------------
    # Encode categorical features
    # ----------------------------

    gender_map = {
        "Female": 0,
        "Male": 1
    }

    married_map = {
        "No": 0,
        "Yes": 1
    }

    dependents_map = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3+": 3
    }

    education_map = {
        "Graduate": 0,
        "Not Graduate": 1
    }

    self_employed_map = {
        "No": 0,
        "Yes": 1
    }

    property_area_map = {
        "Rural": 0,
        "Semiurban": 1,
        "Urban": 2
    }

    gender = gender_map[gender]
    married = married_map[married]
    dependents = dependents_map[dependents]
    education = education_map[education]
    self_employed = self_employed_map[self_employed]
    property_area = property_area_map[property_area]

    # ----------------------------
    # Feature Vector
    # ----------------------------

    features = pd.DataFrame([[
        gender,
        married,
        dependents,
        education,
        self_employed,
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history,
        property_area
    ]], columns=[
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Property_Area"
    ])
    print("Original Features")
    print(features)

    # ----------------------------
    # Scale
    # ----------------------------

    scaled_features = scaler.transform(features)

    print("Scaled Features")
    print(scaled_features)

    # ----------------------------
    # Predict
    # ----------------------------

    prediction = model.predict(scaled_features)

    print("Prediction:", prediction)

    result = "Loan Approved" if prediction[0] == 1 else "Loan Rejected"

    return render_template("index.html", prediction=result)

if(__name__=="__main__"):
    app.run(debug=True)