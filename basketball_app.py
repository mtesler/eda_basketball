from operator import index
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data.
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2022))))

# Web scraping of NBA player stats


@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + \
        str(selected_year) + "_totals.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = df
    raw = raw.fillna(0)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats


player_stats = load_data(selected_year).astype(str)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect(
    'Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_position = ['C', 'PF', 'SF', 'PG', 'SG']
selected_position = st.sidebar.multiselect(
    'Position', unique_position, unique_position)

# Filtering data
df_selected_options = player_stats[(player_stats.Tm.isin(
    selected_team)) & (player_stats.Pos.isin(selected_position))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_options.shape[0]) + ' rows and ' + str(
    df_selected_options.shape[1]) + ' columns')
st.write(df_selected_options)

# Download csv file with NBA player stats data


def file_download(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_options), unsafe_allow_html=True)

# Heatmap
df_selected_options.to_csv('output.csv', index=False)
df = pd.read_csv('output.csv')
