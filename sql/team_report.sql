SELECT teams.team_name as nazwa_druzyny,
       SUM(shots.model_xg) as suma_xg,
       AVG(shots.model_xg) as srednio_xg,
       count(shots.event_id) as liczba_strzalow,
       COUNT(*) FILTER (WHERE shots.outcome = 'Goal') as liczba_goli,
    COUNT(*) FILTER (WHERE shots.outcome = 'Goal') - SUM(shots.model_xg) as roznica_goli_i_xg
FROM shots
INNER JOIN events on events.event_id = shots.event_id
INNER JOIN teams on events.team_id = teams.team_id
GROUP BY teams.team_name
ORDER BY suma_xg DESC
LIMIT 10;