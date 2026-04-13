import psycopg
import json
with psycopg.connect("dbname=statsbomb user=sb password=sbpass host=localhost") as conn:
    with conn.cursor() as curr:
        with open ('input/events_22912.json') as ex:
            ex_data = json.load(ex)
        for event in ex_data:
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