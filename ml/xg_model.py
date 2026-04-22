import psycopg
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

query = """
    SELECT shots.event_id, events.x, events.y, shots.outcome
    FROM shots
    JOIN events ON shots.event_id = events.event_id;
"""

with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    df = pd.read_sql_query(query, conn)

    df['is_goal'] = (df['outcome'] == 'Goal').astype(int)
    df['distance'] = np.sqrt((120-df['x'])**2 + (40 - df['y'])**2)

    kąt_slupek1 = np.arctan2(36 - df['y'], 120 - df['x'])
    kąt_slupek2 = np.arctan2(44 - df['y'], 120 - df['x'])

    df['angle'] = np.abs(kąt_slupek1 - kąt_slupek2) * (180 / np.pi)

    
    X = df[['distance', 'angle']]
    y = df['is_goal']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=69,
        shuffle=True
    )

    cristiano_modaldo = LogisticRegression()
    cristiano_modaldo.fit(X_train,y_train)
    xg_predictions = cristiano_modaldo.predict_proba(X_test)[:, 1]
    
    results = X_test.assign(
    goal_scored=y_test.values,
    xG=xg_predictions
    )
    joblib.dump(cristiano_modaldo,'model_xg.joblib')
    print(results.round(3))
