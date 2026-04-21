import psycopg
import json
with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    with conn.cursor() as curr:
        with open ("/Users/mvtmvch/Documents/GitHub/football-scout/etl/input/matches_43_106.json") as matches_file:
            matches_data = json.load(matches_file)
        for match in matches_data:
            curr.execute(
                "INSERT INTO matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score) " \
                "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (match_id) DO NOTHING;"
                ,(match['match_id'],match['match_date'], match['home_team']['home_team_id'], match['away_team']['away_team_id'], match['home_score'], match['away_score']))
        conn.commit()