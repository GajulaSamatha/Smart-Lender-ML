import pickle
from flask import Flask,render_template

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

if(__name__=="__main__"):
    app.run(debug=True)