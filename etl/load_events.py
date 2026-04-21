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
            with open (f"input/events_{match_id}.json") as ex:
                ex_data = json.load(ex)
                
            for event in ex_data:
                team_info = event.get('team')
                player_info = event.get('player')
                location = event.get('location')
                type_info = event.get('type')

                team_id = team_info.get('id') if team_info else None
                player_id = player_info.get('id') if player_info else None
                x = location[0] if location else None
                y = location[1] if location else None
                event_type = type_info.get('name') if type_info else None
                raw_event = json.dumps(event)

                curr.execute(
                    "INSERT INTO events (event_id, match_id, minute, second, period, event_type, team_id, player_id, x, y, raw_event) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;"
                    ,(event['id'],match_id, event['minute'], event['second'], event['period'], event_type, team_id, player_id, x, y, raw_event))
        conn.commit()