import psycopg
import json
with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    with conn.cursor() as curr:

        matches_id = []
        with open ("/Users/mvtmvch/Documents/GitHub/football-scout/etl/input/matches_43_106.json") as matches_data:
            matches = json.load(matches_data)

        for match in matches:
            matches_id.append(match['match_id'])

        for match_id in matches_id:
            with open (f"input/lineups_{match_id}.json") as lineups_file:
                lineups_data = json.load(lineups_file)
                
            for team in lineups_data:
                curr.execute(
                    "INSERT INTO teams (team_id, team_name) VALUES (%s, %s) ON CONFLICT (team_id) DO NOTHING;"
                    ,(team['team_id'],team['team_name']))
                for players in team['lineup']:
                    print(f"{players['player_name']} - {players['jersey_number']}")
                    curr.execute(
                    "INSERT INTO players (player_name, player_id) VALUES (%s, %s) ON CONFLICT (player_id) DO NOTHING;"
                    ,(players['player_name'],players['player_id']))
        conn.commit()