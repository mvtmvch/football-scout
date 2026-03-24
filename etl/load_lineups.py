import psycopg
import json
with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    with conn.cursor() as curr:
        with open ('input/lineups_22912-2.json') as ex:
            ex_data = json.load(ex)
        for team in ex_data:
            curr.execute(
                "INSERT INTO teams (team_id, team_name) VALUES (%s, %s) ON CONFLICT (team_id) DO NOTHING;"
                ,(team['team_id'],team['team_name']))
            for players in team['lineup']:
                print(f"{players['player_name']} - {players['jersey_number']}")
                curr.execute(
                "INSERT INTO players (player_name, player_id) VALUES (%s, %s) ON CONFLICT (player_id) DO NOTHING;"
                ,(players['player_name'],players['player_id']))
        conn.commit()