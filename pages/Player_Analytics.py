"""
Player Analytics Page
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_players
from utils.preprocessor import get_player_stats
from utils.metrics import calculate_strike_rate, calculate_economy
from components.charts import create_line_chart, create_bar_chart
from components.filters import player_filter
from components.metrics_display import display_kpi_row

st.set_page_config(page_title="Player Analytics", page_icon="👤", layout="wide")

st.title("👤 Player Analytics")
st.markdown("Detailed individual player statistics and performance analysis")

# loading data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

players = get_players(df)

# picking player
selected_player = player_filter(players, key="player_analytics")

# getting stats
with st.spinner(f"Analyzing {selected_player}'s performance..."):
    stats = get_player_stats(df, selected_player)

# showing stats by role
if 'batting' in stats and len(stats['batting']) > 0:
    st.markdown("## 🏏 Batting Statistics")
    
    batting_kpis = {
        "Innings": stats['batting']['innings'],
        "Total Runs": stats['batting']['runs'],
        "Strike Rate": f"{stats['batting']['strike_rate']:.1f}",
        "Average": f"{stats['batting']['average']:.1f}",
        "Fours": stats['batting']['fours'],
        "Sixes": stats['batting']['sixes'],
    }
    display_kpi_row(batting_kpis)
    
    # performance over time
    player_batting = df[df['batter'] == selected_player].copy()
    
    # season runs
    season_runs = player_batting.groupby('year')['runs_batter'].sum().reset_index()
    season_runs.columns = ['Season', 'Runs']
    
    if len(season_runs) > 0:
        fig = create_line_chart(
            season_runs,
            x='Season',
            y='Runs',
            title=f'{selected_player} - Runs by Season'
        )
        st.plotly_chart(fig, width='stretch')
    
    # Performance vs teams
    st.markdown("### Performance vs Different Teams")
    team_perf = player_batting.groupby('bowling_team').agg({
        'runs_batter': 'sum',
        'match_id': 'nunique'
    }).reset_index()
    team_perf.columns = ['Team', 'Runs', 'Innings']
    team_perf = team_perf.sort_values('Runs', ascending=False).head(10)
    
    if len(team_perf) > 0:
        fig = create_bar_chart(
            team_perf,
            x='Team',
            y='Runs',
            title='Top 10 Teams Scored Most Against'
        )
        st.plotly_chart(fig, width='stretch')

if 'bowling' in stats and len(stats['bowling']) > 0:
    st.markdown("## 🎳 Bowling Statistics")
    
    bowling_kpis = {
        "Innings": stats['bowling']['innings'],
        "Wickets": stats['bowling']['wickets'],
        "Economy": f"{stats['bowling']['economy']:.2f}",
        "Average": f"{stats['bowling']['average']:.1f}",
        "Strike Rate": f"{stats['bowling']['strike_rate']:.1f}",
    }
    display_kpi_row(bowling_kpis)
    
    # Performance timeline
    player_bowling = df[df['bowler'] == selected_player].copy()
    
    # Wickets by season
    season_wickets = player_bowling[player_bowling['wicket_kind'].notna()].groupby('year')['wicket_kind'].count().reset_index()
    season_wickets.columns = ['Season', 'Wickets']
    
    if len(season_wickets) > 0:
        fig = create_line_chart(
            season_wickets,
            x='Season',
            y='Wickets',
            title=f'{selected_player} - Wickets by Season'
        )
        st.plotly_chart(fig, width='stretch')
    
    # Performance vs teams
    st.markdown("### Performance vs Different Teams")
    team_wickets = player_bowling[player_bowling['wicket_kind'].notna()].groupby('batting_team').agg({
        'wicket_kind': 'count',
        'match_id': 'nunique'
    }).reset_index()
    team_wickets.columns = ['Team', 'Wickets', 'Innings']
    team_wickets = team_wickets.sort_values('Wickets', ascending=False).head(10)
    
    if len(team_wickets) > 0:
        fig = create_bar_chart(
            team_wickets,
            x='Team',
            y='Wickets',
            title='Top 10 Teams Taken Most Wickets Against'
        )
        st.plotly_chart(fig, width='stretch')

# venue stats
st.markdown("## 🏟️ Venue Performance")

col1, col2 = st.columns(2)

if 'batting' in stats:
    with col1:
        st.markdown("### Batting by Venue")
        player_batting = df[df['batter'] == selected_player]
        venue_batting = player_batting.groupby('venue')['runs_batter'].sum().sort_values(ascending=False).head(10)
        
        if len(venue_batting) > 0:
            st.dataframe(
                venue_batting.reset_index().rename(columns={'venue': 'Venue', 'runs_batter': 'Runs'}),
                width='stretch'
            )

if 'bowling' in stats:
    with col2:
        st.markdown("### Bowling by Venue")
        player_bowling = df[df['bowler'] == selected_player]
        venue_bowling = player_bowling[player_bowling['wicket_kind'].notna()].groupby('venue')['wicket_kind'].count()
        venue_bowling = venue_bowling.sort_values(ascending=False).head(10)
        
        if len(venue_bowling) > 0:
            st.dataframe(
                venue_bowling.reset_index().rename(columns={'venue': 'Venue', 'wicket_kind': 'Wickets'}),
                width='stretch'
            )
