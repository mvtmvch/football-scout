Aplikacja football scout to narzędzie scoutingowo-analityczne, ktore umozliwia analize gry danego zawodnika. 
Pozwala przeanalizować jego okazje bramkowe (xg), podania czy ogolne statystyki.

URUCHOMIENIE BAZY:
cd db
docker compose up -d
by wylaczyc - docker compose down

PARAMETRY POLACZENIA DO BAZY
Host: localhost
Port: 5432
Database: statsbomb
User: sb
Password: sbpass

UTWORZENIE TABEL
Uruchom plik db/schema.sql w DataGrip na źródle statsbomb@localhost.
Po wykonaniu powinny być widoczne tabele: teams, players, matches, events, shots (schema: public).
