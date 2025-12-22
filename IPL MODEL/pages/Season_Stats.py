"""
Season Statistics Page
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_seasons
from utils.preprocessor import get_season_stats
from components.charts import create_bar_chart
from components.filters import season_filter
from components.metrics_display import display_kpi_row

st.set_page_config(page_title="Season Statistics", page_icon="📊", layout="wide")

st.title("📊 Season Statistics")
st.markdown("Comprehensive season-wise analytics and records")

# loading data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

seasons = get_seasons(df)

# picking season
selected_season = season_filter(seasons, key="season_stats")

# getting stats
season_data = get_season_stats(df, selected_season)

# showing metrics
st.markdown(f"## 📈 Season {selected_season} Overview")
kpis = {
    "Total Matches": season_data['total_matches'],
    "Total Runs": f"{season_data['total_runs']:,}",
    "Total Wickets": season_data['total_wickets'],
    "Runs per Match": f"{season_data['total_runs'] / season_data['total_matches']:.0f}" if season_data['total_matches'] > 0 else "0",
}
display_kpi_row(kpis)

# top scorers
st.markdown("## 🧡 Orange Cap Race - Top Run Scorers")

if len(season_data['top_batsmen']) > 0:
    top_batsmen_df = season_data['top_batsmen'].reset_index()
    
    fig = create_bar_chart(
        top_batsmen_df.head(10),
        x='batter',
        y='runs',
        title=f'Top 10 Run Scorers - Season {selected_season}'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show table
    st.dataframe(
        top_batsmen_df.rename(columns={'batter': 'Player', 'runs': 'Runs', 'innings': 'Innings'}),
        use_container_width=True
    )

# top bowlers
st.markdown("## 💜 Purple Cap Race - Top Wicket Takers")

if len(season_data['top_bowlers']) > 0:
    top_bowlers_df = season_data['top_bowlers'].reset_index()
    
    fig = create_bar_chart(
        top_bowlers_df.head(10),
        x='bowler',
        y='wickets',
        title=f'Top 10 Wicket Takers - Season {selected_season}'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show table
    st.dataframe(
        top_bowlers_df.rename(columns={'bowler': 'Player', 'wickets': 'Wickets', 'innings': 'Innings'}),
        use_container_width=True
    )

# boundaries count
st.markdown("## 💥 Boundary Hitters")

season_df = df[df['year'] == selected_season]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Most Sixes")
    sixes = season_df[season_df['runs_batter'] == 6].groupby('batter')['runs_batter'].count()
    sixes = sixes.sort_values(ascending=False).head(10)
    
    st.dataframe(
        sixes.reset_index().rename(columns={'batter': 'Player', 'runs_batter': 'Sixes'}),
        use_container_width=True
    )

with col2:
    st.markdown("### Most Fours")
    fours = season_df[season_df['runs_batter'] == 4].groupby('batter')['runs_batter'].count()
    fours = fours.sort_values(ascending=False).head(10)
    
    st.dataframe(
        fours.reset_index().rename(columns={'batter': 'Player', 'runs_batter': 'Fours'}),
        use_container_width=True
    )

# team rankings
st.markdown("## 🏆 Team Performance")

team_stats = []
teams_in_season = set(season_df['batting_team'].unique()) | set(season_df['bowling_team'].unique())

for team in teams_in_season:
    team_data = season_df[(season_df['batting_team'] == team) | (season_df['bowling_team'] == team)]
    matches = team_data['match_id'].nunique()
    wins = team_data[team_data['match_won_by'] == team]['match_id'].nunique()
    
    team_stats.append({
        'Team': team,
        'Matches': matches,
        'Wins': wins,
        'Losses': matches - wins,
        'Win %': (wins / matches * 100) if matches > 0 else 0
    })

team_standings = pd.DataFrame(team_stats).sort_values('Win %', ascending=False)

if len(team_standings) > 0:
    fig = create_bar_chart(
        team_standings,
        x='Team',
        y='Win %',
        title=f'Team Win Percentage - Season {selected_season}',
        color='Team'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(team_standings, use_container_width=True)

# best partnerships
st.markdown("## 🤝 Top Partnerships")

# Calculate partnerships (runs scored together)
partnerships = season_df.groupby(['batting_partners', 'match_id'])['runs_total'].sum()
partnerships = partnerships.sort_values(ascending=False).head(10)

if len(partnerships) > 0:
    partnerships_df = partnerships.reset_index()
    partnerships_df.columns = ['Partnership', 'Match ID', 'Runs']
    
    st.dataframe(
        partnerships_df[['Partnership', 'Runs']],
        use_container_width=True
    )

# highest scores
st.markdown("## 📈 Highest Team Totals")

highest_totals = season_df.groupby(['batting_team', 'match_id']).agg({
    'team_runs': 'max',
    'venue': 'first',
    'bowling_team': 'first'
}).reset_index()

highest_totals = highest_totals.sort_values('team_runs', ascending=False).head(10)
highest_totals.columns = ['Team', 'Match ID', 'Runs', 'Venue', 'Opposition']

st.dataframe(
    highest_totals[['Team', 'Runs', 'Opposition', 'Venue']],
    use_container_width=True
)
