"""
Team Analytics Page
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data, get_teams, get_seasons
from utils.preprocessor import get_team_stats
from components.charts import create_bar_chart, create_line_chart, create_pie_chart
from components.filters import team_filter, season_filter
from components.metrics_display import display_kpi_row
import config

st.set_page_config(page_title="Team Analytics", page_icon="🏏", layout="wide")

st.title("🏏 Team Analytics")
st.markdown("Comprehensive team statistics and performance analysis")

# load Data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

teams = get_teams(df)
seasons = get_seasons(df)

# filtering options
col1, col2 = st.columns([1, 3])
with col1:
    selected_team = team_filter(teams, key="team_analytics")

# calc stats
with st.spinner("Calculating team statistics..."):
    team_data = df[(df['batting_team'] == selected_team) | (df['bowling_team'] == selected_team)]
    stats = get_team_stats(df, selected_team)

# show KPIs
st.markdown("## 📈 Overall Performance")
kpis = {
    "Total Matches": stats['total_matches'],
    "Matches Won": stats['matches_won'],
    "Win %": f"{stats['win_percentage']:.1f}%",
    "Strike Rate": f"{stats['batting_strike_rate']:.1f}",
}
display_kpi_row(kpis)

# season stats
st.markdown("## 📊 Season-wise Performance")
season_stats = []
for year in seasons:
    year_data = team_data[team_data['year'] == year]
    matches = year_data['match_id'].nunique()
    wins = year_data[year_data['match_won_by'] == selected_team]['match_id'].nunique()
    
    season_stats.append({
        'Season': year,
        'Matches': matches,
        'Wins': wins,
        'Win %': (wins/matches*100) if matches > 0 else 0
    })

season_df = pd.DataFrame(season_stats)

if len(season_df) > 0:
    fig = create_line_chart(
        season_df,
        x='Season',
        y='Win %',
        title=f'{selected_team} - Win % by Season'
    )
    st.plotly_chart(fig, use_container_width=True)

# venue stuff
st.markdown("## 🏟️ Venue-wise Performance")
venue_stats = team_data.groupby('venue').agg({
    'match_id': 'nunique',
}).rename(columns={'match_id': 'Matches'})

venue_wins = team_data[team_data['match_won_by'] == selected_team].groupby('venue')['match_id'].nunique()
venue_stats['Wins'] = venue_wins
venue_stats['Wins'] = venue_stats['Wins'].fillna(0)
venue_stats['Win %'] = (venue_stats['Wins'] / venue_stats['Matches'] * 100).round(1)
venue_stats = venue_stats.sort_values('Matches', ascending=False).head(10)

if len(venue_stats) > 0:
    fig = create_bar_chart(
        venue_stats.reset_index(),
        x='venue',
        y='Win %',
        title='Top 10 Venues by Win %',
        orientation='v'
    )
    st.plotly_chart(fig, use_container_width=True)

# analyzing toss
st.markdown("## 🪙 Toss Decision Analysis")
col1, col2 = st.columns(2)

with col1:
    toss_data = team_data[team_data['toss_winner'] == selected_team]
    toss_decisions = toss_data.groupby('toss_decision')['match_id'].nunique()
    
    if len(toss_decisions) > 0:
        fig = create_pie_chart(
            values=toss_decisions.values,
            names=toss_decisions.index,
            title='Toss Decisions When Won'
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    toss_wins = team_data[team_data['toss_winner'] == selected_team]['match_id'].nunique()
    toss_and_match = team_data[(team_data['toss_winner'] == selected_team) & 
                                (team_data['match_won_by'] == selected_team)]['match_id'].nunique()
    
    st.metric("Tosses Won", toss_wins)
    st.metric("Matches Won After Winning Toss", toss_and_match)
    if toss_wins > 0:
        st.metric("Win % After Winning Toss", f"{(toss_and_match/toss_wins*100):.1f}%")

# best players
st.markdown("## ⭐ Top Performers")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top Run Scorers")
    batting = team_data.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)
    st.dataframe(batting.reset_index().rename(columns={'batter': 'Player', 'runs_batter': 'Runs'}), 
                 use_container_width=True)

with col2:
    st.markdown("### Top Wicket Takers")
    wickets = team_data[team_data['wicket_kind'].notna()].groupby('bowler')['wicket_kind'].count()
    wickets = wickets.sort_values(ascending=False).head(10)
    st.dataframe(wickets.reset_index().rename(columns={'bowler': 'Player', 'wicket_kind': 'Wickets'}),
                 use_container_width=True)
