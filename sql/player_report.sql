SELECT count(shots.event_id) as liczba_strzalow,
       SUM(shots.model_xg) as suma_xg,
       AVG(shots.model_xg) as srednio_xg,
       players.player_name as imie_zawodnika,
       teams.team_name as nazwa_druzyny,
       COUNT(*) FILTER (WHERE shots.outcome = 'Goal') as liczba_goli,
       SUM(shots.model_xg) - COUNT(*) FILTER (WHERE shots.outcome = 'Goal')  as roznica_goli_i_xg
FROM shots
INNER JOIN events on events.event_id = shots.event_id
INNER JOIN players on players.player_id = events.player_id
INNER JOIN teams on events.team_id = teams.team_id
GROUP BY players.player_name,
teams.team_name
ORDER BY suma_xg DESC
LIMIT 10;