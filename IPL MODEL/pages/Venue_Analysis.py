"""
Venue Analysis Page
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_venues, get_teams
from utils.preprocessor import get_venue_stats
from components.charts import create_bar_chart, create_pie_chart
from components.filters import venue_filter
from components.metrics_display import display_kpi_row

st.set_page_config(page_title="Venue Analysis", page_icon="🏟️", layout="wide")

st.title("🏟️ Venue Analysis")
st.markdown("Comprehensive venue statistics and pitch behavior insights")

# loading stuff
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

venues = get_venues(df)
teams = get_teams(df)

# pick venue
selected_venue = venue_filter(venues, key="venue_analysis")

# calc stats
venue_data = df[df['venue'] == selected_venue].copy()
stats = get_venue_stats(df, selected_venue)

# key metrics
st.markdown("## 📈 Venue Overview")
kpis = {
    "Total Matches": stats['total_matches'],
    "Avg 1st Innings": f"{stats['avg_score_innings1']:.0f}",
    "Avg 2nd Innings": f"{stats['avg_score_innings2']:.0f}",
    "Highest Score": int(stats['highest_score']),
}
display_kpi_row(kpis)

# bat 1st vs 2nd
st.markdown("## 🎯 Bat First vs Chase Analysis")

col1, col2 = st.columns(2)

with col1:
    innings_comparison = pd.DataFrame({
        'Innings': ['1st Innings', '2nd Innings'],
        'Average Score': [stats['avg_score_innings1'], stats['avg_score_innings2']]
    })
    
    fig = create_bar_chart(
        innings_comparison,
        x='Innings',
        y='Average Score',
        title='Average Score Comparison'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
   # Win percentage by batting first
    toss_bat_first = venue_data[venue_data['toss_decision'] == 'bat'].groupby('match_id').first()
    bat_first_wins_team = toss_bat_first[toss_bat_first['match_won_by'] == toss_bat_first['toss_winner']]
    
    toss_field_first = venue_data[venue_data['toss_decision'] == 'field'].groupby('match_id').first()
    field_first_wins_team = toss_field_first[toss_field_first['match_won_by'] == toss_field_first['toss_winner']]
    
    bat_first_total = len(toss_bat_first)
    field_first_total = len(toss_field_first)
    
    bat_first_wins = len(bat_first_wins_team)
    chase_wins = len(field_first_wins_team)
    
    if bat_first_total + field_first_total > 0:
        win_data = pd.DataFrame({
            'Decision': ['Bat First', 'Chase'],
            'Matches Won': [bat_first_wins, chase_wins]
        })
        
        fig = create_pie_chart(
            values=win_data['Matches Won'].values,
            names=win_data['Decision'].values,
            title='Win Distribution by Toss Decision'
        )
        st.plotly_chart(fig, use_container_width=True)

# how teams play here
st.markdown("## 🏏 Team Performance at Venue")

team_performance = []
for team in teams:
    team_data = venue_data[(venue_data['batting_team'] == team) | (venue_data['bowling_team'] == team)]
    matches = team_data['match_id'].nunique()
    
    if matches > 0:
        wins = team_data[team_data['match_won_by'] == team]['match_id'].nunique()
        win_pct = (wins / matches * 100) if matches > 0 else 0
        
        team_performance.append({
            'Team': team,
            'Matches': matches,
            'Wins': wins,
            'Win %': win_pct
        })

team_perf_df = pd.DataFrame(team_performance).sort_values('Matches', ascending=False).head(10)

if len(team_perf_df) > 0:
    fig = create_bar_chart(
        team_perf_df,
        x='Team',
        y='Win %',
        title='Top 10 Teams by Win % at Venue',
        color='Team'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(team_perf_df, use_container_width=True)

# phase analysis
st.markdown("## ⚡ Phase-wise Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Powerplay (Overs 1-6)")
    powerplay_data = venue_data[venue_data['over'] < 6]
    
    pp_runs = powerplay_data.groupby('match_id')['team_runs'].max().mean()
    pp_wickets = powerplay_data.groupby('match_id')['team_wicket'].max().mean()
    
    st.metric("Avg Runs", f"{pp_runs:.1f}")
    st.metric("Avg Wickets", f"{pp_wickets:.1f}")

with col2:
    st.markdown("### Death Overs (16-20)")
    death_data = venue_data[venue_data['over'] >= 15]
    
    death_runs_per_match = death_data.groupby('match_id')['runs_total'].sum().mean()
    death_wickets = death_data[death_data['wicket_kind'].notna()].groupby('match_id')['wicket_kind'].count().mean()
    
    st.metric("Avg Runs", f"{death_runs_per_match:.1f}")
    st.metric("Avg Wickets", f"{death_wickets:.1f}")

# best games
st.markdown("## ⭐ Top Performances at Venue")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Highest Individual Scores")
    top_scores = venue_data.groupby(['batter', 'match_id'])['runs_batter'].sum()
    top_scores = top_scores.sort_values(ascending=False).head(10)
    
    top_scores_df = top_scores.reset_index()
    top_scores_df.columns = ['Player', 'Match ID', 'Runs']
    st.dataframe(top_scores_df[['Player', 'Runs']], use_container_width=True)

with col2:
    st.markdown("### Best Bowling Figures")
    bowling_data = venue_data[venue_data['wicket_kind'].notna()]
    top_bowling = bowling_data.groupby(['bowler', 'match_id'])['wicket_kind'].count()
    top_bowling = top_bowling.sort_values(ascending=False).head(10)
    
    top_bowling_df = top_bowling.reset_index()
    top_bowling_df.columns = ['Player', 'Match ID', 'Wickets']
    st.dataframe(top_bowling_df[['Player', 'Wickets']], use_container_width=True)

# trends over years
st.markdown("## 📊 Season-wise Trends")

season_stats = venue_data.groupby('year').agg({
    'match_id': 'nunique',
    'runs_total': 'sum'
}).reset_index()
season_stats.columns = ['Season', 'Matches', 'Total Runs']
season_stats['Avg Runs per Match'] = (season_stats['Total Runs'] / season_stats['Matches']).round(0)

if len(season_stats) > 0:
    from components.charts import create_line_chart
    fig = create_line_chart(
        season_stats,
        x='Season',
        y='Avg Runs per Match',
        title='Average Runs per Match Over Seasons'
    )
    st.plotly_chart(fig, use_container_width=True)
