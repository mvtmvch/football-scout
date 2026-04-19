import psycopg
import pandas as pd
import numpy as np
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

    print(df[['outcome', 'is_goal', 'distance', 'angle']].head())
