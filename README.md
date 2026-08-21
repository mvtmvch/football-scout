# Football Scout ⚽

**Football Scout** is an end-to-end football analytics project built around event data from **StatsBomb Open Data**.

The application transforms raw match data into a PostgreSQL database, estimates **expected goals (xG)** with a machine learning model, exposes analytical reports through a **FastAPI REST API**, and presents the results in an interactive **Streamlit dashboard**.

The project was built to practice the complete data workflow — from raw sports data and ETL, through SQL and machine learning, to an API and a user-facing analytical dashboard.

![Football Scout Dashboard](docs/dashboard.png)

## Key Features

- **Football data ETL** — loads teams, players, matches, events and shots from StatsBomb JSON files into PostgreSQL.
- **Relational PostgreSQL database** — structured storage for match and event-level data.
- **xG model** — logistic regression model estimating goal probability from shot distance and shooting angle.
- **Player analytics** — reports including shots, goals, total xG, average xG and goals/xG comparison.
- **Team analytics** — aggregated team-level shooting and xG statistics.
- **Shot-level analysis** — inspect individual shots for a selected player, including location, outcome and predicted xG.
- **REST API** — FastAPI endpoints serving model predictions and analytical reports.
- **Interactive dashboard** — Streamlit interface for exploring players, teams and selected metrics.

## Architecture

```text
StatsBomb Open Data
        │
        ▼
   ETL scripts
        │
        ▼
    PostgreSQL
     ┌──┴─────────────┐
     │                │
     ▼                ▼
 SQL reports       xG model
     │                │
     └───────┬────────┘
             ▼
          FastAPI
             │
             ▼
         Streamlit
         Dashboard
```

## Tech Stack

| Area | Technologies |
| --- | --- |
| Programming | Python |
| Data processing | pandas, NumPy |
| Database | PostgreSQL, SQL |
| Machine learning | scikit-learn, joblib |
| API | FastAPI |
| Dashboard | Streamlit |
| Database access | psycopg |
| Infrastructure | Docker Compose |

## xG Model

The project includes a baseline **expected goals model** implemented with logistic regression.

For every shot, two features are calculated from the StatsBomb pitch coordinates:

- **distance** from the shot location to the centre of the goal,
- **angle** between the shot location and the two goalposts.

The target variable indicates whether the shot resulted in a goal.

```text
shot location (x, y)
        │
        ├──► distance to goal
        │
        └──► shooting angle
                  │
                  ▼
        Logistic Regression
                  │
                  ▼
            xG probability
```

The trained model is stored as:

```text
ml/model_xg.joblib
```

Predictions can be generated for individual shots through the API or written back to the `shots.model_xg` column for further SQL analysis.

This is intentionally a **baseline xG model**. Its purpose is to demonstrate the full modelling workflow rather than reproduce a production-grade football analytics model.

## Dashboard

The Streamlit dashboard provides two main analytical views:

### Team reports

Teams can be compared using metrics such as:

- total generated xG,
- goals scored,
- goals compared with xG,
- number of shots,
- average xG per shot.

Results are available both as a table and as a ranked bar chart.

### Player reports

The player view provides similar aggregated metrics at player level and additionally allows a user to select an individual player and inspect their shots.

For each shot, the application can display:

- match,
- minute and second,
- shot outcome,
- predicted xG,
- shot coordinates.

## API

The FastAPI application is defined in [`api.py`](api.py).

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/predict` | Predict xG from shot distance and angle |
| `GET` | `/teams/report` | Return aggregated team analytics |
| `GET` | `/players/report` | Return aggregated player analytics |
| `GET` | `/players/shots` | Return shot-level data for a selected player |

### Example

```http
GET /predict?distance=15&angle=25
```

Example response:

```json
{
  "xg": 0.18
}
```

FastAPI's interactive API documentation is available at:

```text
/docs
```

while the API is running.

## Database

The PostgreSQL schema is defined in [`db/schema.sql`](db/schema.sql).

The database contains five main tables:

```text
teams
players
matches
events
shots
```

### Relationships

```text
teams
  │
  ├──── matches
  │
  └──── events
           │
           ├──── players
           │
           └──── shots
```

The `events` table stores general event information together with the original event JSON, while the `shots` table contains shot-specific data and model-generated xG values.

Indexes are included for commonly queried event and xG fields.

## Project Structure

```text
football-scout/
│
├── api.py
│
├── dashboard/
│   └── app.py
│
├── db/
│   ├── docker-compose.yml
│   └── schema.sql
│
├── etl/
│   ├── explore_data.py
│   ├── load_lineups.py
│   ├── load_matches.py
│   ├── load_events.py
│   └── load_shots.py
│
├── ml/
│   ├── xg_model.py
│   ├── fill_xg.py
│   └── model_xg.joblib
│
└── sql/
    ├── team_report.sql
    ├── player_report.sql
    └── player_shots.sql
```

## Running the Project Locally

### Requirements

- Python 3.9+
- Docker
- Docker Compose

### 1. Create a virtual environment

```bash
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn streamlit pandas numpy scikit-learn joblib "psycopg[binary]" requests
```

### 3. Start PostgreSQL

```bash
cd db
docker compose up -d
cd ..
```

The local development database uses:

```text
Host: localhost
Port: 5432
Database: statsbomb
User: sb
Password: sbpass
```

### 4. Create the database schema

Using `psql`:

```bash
psql -h localhost -U sb -d statsbomb -f db/schema.sql
```

The same SQL file can also be executed through a database client such as DataGrip.

## Preparing the Data

The ETL scripts work with StatsBomb-style JSON data.

They expect:

```text
matches_43_106.json
input/events_<match_id>.json
input/lineups_<match_id>.json
```

The current ETL scripts contain a locally configured path to `matches_43_106.json`, so this path may need to be adjusted before running them on another machine.

After preparing the data, run the ETL scripts in the following order:

```bash
cd etl

python load_lineups.py
python load_matches.py
python load_events.py
python load_shots.py
```

The order is important because teams and players are loaded before matches and events that reference them.

## Training and Applying the xG Model

After the shot data has been loaded:

```bash
cd ../ml

python xg_model.py
python fill_xg.py

cd ..
```

`xg_model.py` trains the logistic regression model and saves it as `model_xg.joblib`.

`fill_xg.py` uses the trained model to calculate xG values for shots where `model_xg` has not yet been populated.

## Starting the API

From the project root:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

## Starting the Dashboard

In a second terminal:

```bash
streamlit run dashboard/app.py
```

The dashboard communicates with the locally running FastAPI service.

## SQL Analytics

The analytical queries are separated from the API code and stored in the [`sql/`](sql/) directory.

### `team_report.sql`

Aggregates shooting performance by team, including:

- total xG,
- average xG,
- shots,
- goals,
- goals/xG difference.

### `player_report.sql`

Calculates equivalent metrics for individual players and associates each player with their team.

### `player_shots.sql`

Returns detailed shot data for a selected player, including:

- match ID,
- timestamp,
- outcome,
- xG,
- shot coordinates.

## Current Scope

Football Scout is a learning and portfolio project focused on demonstrating an end-to-end football data workflow.

The current version focuses primarily on **shot-based analysis and xG** rather than providing a complete professional scouting platform.

## Possible Next Steps

Future improvements could include:

- replacing machine-specific ETL paths with configurable relative paths or CLI arguments,
- moving database credentials to environment variables,
- adding `requirements.txt` or `pyproject.toml`,
- adding automated tests,
- adding model evaluation and calibration metrics,
- expanding the xG model with additional shot features,
- adding shot maps and pitch visualisations,
- adding filters for competitions, matches and time periods,
- containerising the API and dashboard,
- deploying the application as a complete web service.

## Author

**Mateusz Michalski**

Applied Computer Science student interested in data analysis, software development and football analytics.