from fastapi import FastAPI
import pickle
import pandas as pd
import os

app = FastAPI()

# -------- LOAD MODEL --------
model = None
vectorizer = None

try:
    path = "backend/models/classifier.pkl"
    if os.path.exists(path):
        model, vectorizer = pickle.load(open(path, "rb"))
        print("✅ Model loaded")
    else:
        print("❌ Model not found")
except Exception as e:
    print("Error loading model:", e)

# -------- HOME --------
@app.get("/")
def home():
    return {"message": "Urban Safety API Running 🚀"}

# -------- PREDICT --------
@app.post("/predict")
def predict(text: str):
    if model is None:
        return {"error": "Model not loaded"}

    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]

    return {"crime_type": pred}

# -------- HOTSPOTS --------
@app.get("/hotspots")
def hotspots():
    df = pd.read_csv("data/crime_data.csv")
    return df.to_dict(orient="records")