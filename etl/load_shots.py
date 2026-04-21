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
            with open (f"input/events_{match_id}.json") as shots_file:
                shots_data = json.load(shots_file)

            for event in shots_data:
                type_info = event.get('type')
                if not type_info or type_info.get('name') != 'Shot':
                    continue

                shot_info = event.get('shot', {})
                outcome = shot_info.get('outcome', {}).get('name')
                raw_shot = json.dumps(shot_info)

                curr.execute(
                    "INSERT INTO shots (event_id, model_xg, outcome, raw_shot) " \
                    "VALUES (%s, NULL, %s, %s) ON CONFLICT (event_id) DO NOTHING;"
                    ,(event['id'], outcome, raw_shot))
        conn.commit()