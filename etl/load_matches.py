import psycopg
import json
with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    with conn.cursor() as curr:
        with open ('input/matches_4.json') as ex:
            ex_data = json.load(ex)
        for match in ex_data:
            curr.execute(
                "INSERT INTO matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score) " \
                "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (match_id) DO NOTHING;"
                ,(match['match_id'],match['match_date'], match['home_team']['home_team_id'], match['away_team']['away_team_id'], match['home_score'], match['away_score']))
        conn.commit()