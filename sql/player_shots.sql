SELECT players.player_name as imie_zawodnika,
       teams.team_name as nazwa_druzyny,
       matches.match_id,
       events.minute as minute,
       events.second as seconds,
       shots.outcome as outcome,
       shots.model_xg as xg,
       events.x as x,
       events.y as y
FROM shots
INNER JOIN events on events.event_id = shots.event_id
INNER JOIN players on players.player_id = events.player_id
INNER JOIN teams on events.team_id = teams.team_id
INNER JOIN matches on matches.match_id = events.match_id
WHERE players.player_name ILIKE %(player_name)s
ORDER BY matches.match_id DESC, events.minute, events.second;

