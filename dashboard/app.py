import streamlit as st
import pandas as pd
import requests

st.title("Football Scout Dashboard")
response = requests.get("http://127.0.0.1:8000/teams/report")
data_t = response.json()
df_t = pd.DataFrame(data_t)

response = requests.get("http://127.0.0.1:8000/players/report")
data_p = response.json()
df_p = pd.DataFrame(data_p)

view = st.sidebar.selectbox(
    "Wybierz raport",
    ["Drużyny", "Zawodnicy"])

metric_choice = st.sidebar.selectbox(
    "Wybierz metrykę",
    ["suma wygenerowanego xg", "suma strzelonych goli",
    "over/underperformance względem xG"])

top_n = st.sidebar.slider(
    "ile rekordów pokazać?",
    min_value=5,
    max_value=30,
    value=10
)

if metric_choice == "suma wygenerowanego xg":
    col = "suma_xg"
elif metric_choice == "suma strzelonych goli":
    col = "liczba_goli"
elif metric_choice == "over/underperformance względem xG":
    col = "roznica_goli_i_xg"

if view == "Drużyny":
    st.subheader("Raport drużyn pod względem wybranej metryki")
    st.dataframe(df_t.set_index("nazwa_druzyny"))
    st.subheader("Wykres pokazujący wygenerowane xg zespołów")
    st.bar_chart(df_t.set_index("nazwa_druzyny")[col].sort_values(ascending=False).head(top_n))
else:
    st.subheader("Raport zawodników pod względem wybranej metryki")
    st.dataframe(df_p.set_index("imie_zawodnika"))
    st.subheader("Wykres pokazujący wygenerowane xg zawodników")
    st.bar_chart(df_p.set_index("imie_zawodnika")[col].sort_values(ascending=False).head(top_n))
