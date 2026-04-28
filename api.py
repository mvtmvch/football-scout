from pathlib import Path
from fastapi import FastAPI
import joblib
import pandas as pd
import psycopg

app =  FastAPI()
model = joblib.load('ml/model_xg.joblib')

@app.get("/predict")
def count_xg(distance:float, angle:float):
    data=pd.DataFrame([{'distance' : distance, 'angle' : angle}])
    proba_goal = model.predict_proba(data)[0, 1]
    return {"xg": float(proba_goal)}

@app.get("/teams/report")
def show_report():
    query = Path('sql/team_report.sql').read_text()
    with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
        df = pd.read_sql_query(query, conn)
        return df.to_dict(orient="records")
    
@app.get("/players/report")
def show_report():
    query = Path('sql/player_report.sql').read_text()
    with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
        df = pd.read_sql_query(query, conn)
        return df.to_dict(orient="records")