"""
Head-to-Head Analysis Page
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_teams
from utils.preprocessor import get_head_to_head
from components.charts import create_pie_chart, create_bar_chart, create_radar_chart
from components.metrics_display import display_kpi_row
import config

st.set_page_config(page_title="Head-to-Head", page_icon="⚔️", layout="wide")

st.title("⚔️ Head-to-Head Analysis")
st.markdown("Compare two teams and analyze their historical matchups")

# load Data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

teams = get_teams(df)

# picking teams
col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Select Team 1", teams, key="h2h_team1")

with col2:
    team2_options = [t for t in teams if t != team1]
    team2 = st.selectbox("Select Team 2", team2_options, key="h2h_team2")

# calc h2h
h2h_stats = get_head_to_head(df, team1, team2)

# showing record
st.markdown("## 🏆 Overall Head-to-Head Record")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; color: white;">
            <h3>{team1}</h3>
            <h1>{h2h_stats['team1_wins']}</h1>
            <p>Wins ({h2h_stats['team1_win_pct']:.1f}%)</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f5f5f5; 
                    border-radius: 10px;">
            <h3>Total Matches</h3>
            <h1>{h2h_stats['total_matches']}</h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); 
                    border-radius: 10px; color: white;">
            <h3>{team2}</h3>
            <h1>{h2h_stats['team2_wins']}</h1>
            <p>Wins ({h2h_stats['team2_win_pct']:.1f}%)</p>
        </div>
    """, unsafe_allow_html=True)

# who won more
st.markdown("## 📊 Win Distribution")
if h2h_stats['total_matches'] > 0:
    fig = create_pie_chart(
        values=[h2h_stats['team1_wins'], h2h_stats['team2_wins']],
        names=[team1, team2],
        title="Head-to-Head Win Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# stats by venue
st.markdown("## 🏟️ Venue-wise Performance")

h2h_df = df[
    ((df['batting_team'] == team1) & (df['bowling_team'] == team2)) |
    ((df['batting_team'] == team2) & (df['bowling_team'] == team1))
].copy()

venue_h2h = []
for venue in h2h_df['venue'].unique():
    venue_data = h2h_df[h2h_df['venue'] == venue]
    total = venue_data['match_id'].nunique()
    team1_wins = venue_data[venue_data['match_won_by'] == team1]['match_id'].nunique()
    team2_wins = venue_data[venue_data['match_won_by'] == team2]['match_id'].nunique()
    
    venue_h2h.append({
        'Venue': venue,
        f'{team1} Wins': team1_wins,
        f'{team2} Wins': team2_wins,
        'Total': total
    })

venue_df = pd.DataFrame(venue_h2h).sort_values('Total', ascending=False).head(10)

if len(venue_df) > 0:
    st.dataframe(venue_df, use_container_width=True)

# last 10 matches
st.markdown("## 📈 Recent Form (Last 10 Matches)")

recent_matches = h2h_df.groupby('match_id').agg({
    'date': 'first',
    'match_won_by': 'first',
    'venue': 'first'
}).sort_values('date', ascending=False).head(10)

if len(recent_matches) > 0:
    recent_matches['Winner'] = recent_matches['match_won_by']
    recent_matches['Date'] = recent_matches['date'].dt.strftime('%Y-%m-%d')
    recent_matches['Venue'] = recent_matches['venue']
    
    st.dataframe(
        recent_matches[['Date', 'Winner', 'Venue']].reset_index(drop=True),
        use_container_width=True
    )

# stat compare
st.markdown("## 📊 Statistical Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {team1}")
    team1_data = h2h_df[h2h_df['batting_team'] == team1]
    
    if len(team1_data) > 0:
        runs = team1_data.groupby('match_id')['team_runs'].max().mean()
        wickets = team1_data.groupby('match_id')['team_wicket'].max().mean()
        
        st.metric("Avg Score", f"{runs:.1f}")
        st.metric("Avg Wickets Lost", f"{wickets:.1f}")

with col2:
    st.markdown(f"### {team2}")
    team2_data = h2h_df[h2h_df['batting_team'] == team2]
    
    if len(team2_data) > 0:
        runs = team2_data.groupby('match_id')['team_runs'].max().mean()
        wickets = team2_data.groupby('match_id')['team_wicket'].max().mean()
        
        st.metric("Avg Score", f"{runs:.1f}")
        st.metric("Avg Wickets Lost", f"{wickets:.1f}")

# top players here
st.markdown("## ⭐ Top Performers in H2H Matches")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top Run Scorers")
    top_batsmen = h2h_df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)
    st.dataframe(
        top_batsmen.reset_index().rename(columns={'batter': 'Player', 'runs_batter': 'Runs'}),
        use_container_width=True
    )

with col2:
    st.markdown("### Top Wicket Takers")
    top_bowlers = h2h_df[h2h_df['wicket_kind'].notna()].groupby('bowler')['wicket_kind'].count()
    top_bowlers = top_bowlers.sort_values(ascending=False).head(10)
    st.dataframe(
        top_bowlers.reset_index().rename(columns={'bowler': 'Player', 'wicket_kind': 'Wickets'}),
        use_container_width=True
    )
