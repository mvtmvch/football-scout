import json
with open ('input/lineups_22912-2.json') as ex:
    ex_data = json.load(ex)
for team in ex_data:
    print(f"druzyna - {team['team_name']}, id - {team['team_id']}")
    for players in team['lineup']:
        print(f"{players['player_name']} - {players['jersey_number']}")