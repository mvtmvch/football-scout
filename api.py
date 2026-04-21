from fastapi import FastAPI
import joblib
import pandas as pd

app =  FastAPI()
model = joblib.load('ml/model_xg.joblib')

@app.get("/predict")
def count_xg(distance:float, angle:float):
    data=pd.DataFrame([{'distance' : distance, 'angle' : angle}])
    proba_goal = model.predict_proba(data)[0, 1]
    return {"xg": float(proba_goal)}
