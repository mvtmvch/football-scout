CREATE TABLE teams(
    team_id BIGINT PRIMARY KEY,
    team_name TEXT NOT NULL
);

CREATE TABLE players(
    player_id BIGINT PRIMARY KEY ,
    player_name TEXT NOT NULL
);
CREATE TABLE matches(
    match_id BIGINT PRIMARY KEY,
    match_date date,
    home_team_id BIGINT references teams(team_id),
    away_team_id BIGINT references teams(team_id),
    home_score int,
    away_score int
);
CREATE TABLE events(
    event_id uuid PRIMARY KEY,
    match_id BIGINT NOT NULL references matches(match_id) on delete cascade,
    minute int,
    second int,
    period int,
    event_type TEXT,
    team_id BIGINT references teams(team_id),
    player_id BIGINT references players(player_id),
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    raw_event JSONB
);
CREATE TABLE shots(
    event_id uuid PRIMARY KEY references events(event_id) on delete cascade ,
    model_xg DOUBLE PRECISION,
    outcome TEXT,
    raw_shot JSONB
);
CREATE INDEX IF NOT EXISTS idx_events_match       ON events(match_id);
CREATE INDEX IF NOT EXISTS idx_events_match_type  ON events(match_id, event_type);
CREATE INDEX IF NOT EXISTS idx_events_player      ON events(player_id);
CREATE INDEX IF NOT EXISTS idx_shots_modelxg      ON shots(model_xg);