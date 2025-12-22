"""
Match Simulator Page
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data, get_matches
from components.charts import create_line_chart

st.set_page_config(page_title="Match Simulator", page_icon="🎮", layout="wide")

st.title("🎮 Match Simulator")
st.markdown("Replay historical IPL matches ball-by-ball")

# loading data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

# fetch matches
matches = get_matches(df)

# pick match
st.markdown("## 🏏 Select a Match")

# create match desc
matches['match_desc'] = (
    matches['date'].dt.strftime('%Y-%m-%d') + ' - ' +
    matches['batting_team'] + ' vs ' + matches['bowling_team'] +
    ' @ ' + matches['venue']
)

selected_match_desc = st.selectbox(
    "Choose a match to simulate",
    matches['match_desc'].head(100).tolist(),  # Limit to recent 100 matches
    key="match_simulator"
)

if selected_match_desc:
    # Get the selected match data
    selected_match_id = matches[matches['match_desc'] == selected_match_desc]['match_id'].iloc[0]
    match_data = df[df['match_id'] == selected_match_id].copy()
    
    # match details
    st.markdown("---")
    st.markdown("## 📋 Match Information")
    
    match_info = match_data.iloc[0]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Date:** {match_info['date'].strftime('%d %B %Y')}")
        st.markdown(f"**Venue:** {match_info['venue']}")
    
    with col2:
        st.markdown(f"**Toss Winner:** {match_info['toss_winner']}")
        st.markdown(f"**Toss Decision:** {match_info['toss_decision']}")
    
    with col3:
        st.markdown(f"**Winner:** {match_info['match_won_by']}")
        st.markdown(f"**Win Margin:** {match_info['win_outcome']}")
    
    # score chart
    st.markdown("## 📊 Score Progression")
    
    # Calculate cumulative runs for each innings
    innings_data = []
    
    for innings in match_data['innings'].unique():
        innings_df = match_data[match_data['innings'] == innings].copy()
        innings_df = innings_df.sort_values(['over', 'ball'])
        innings_df['cumulative_runs'] = innings_df['runs_total'].cumsum()
        innings_df['ball_number'] = range(1, len(innings_df) + 1)
        
        batting_team = innings_df['batting_team'].iloc[0]
        
        innings_data.append({
            'innings': innings,
            'team': batting_team,
            'data': innings_df
        })
    
    # Create score progression chart
    fig = go.Figure()
    
    for inning in innings_data:
        fig.add_trace(go.Scatter(
            x=inning['data']['ball_number'],
            y=inning['data']['cumulative_runs'],
            mode='lines',
            name=f"{inning['team']} (Innings {inning['innings']})",
            hovertemplate='<b>Ball:</b> %{x}<br><b>Score:</b> %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Score Progression",
        xaxis_title="Ball Number",
        yaxis_title="Cumulative Runs",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # wickets timeline
    st.markdown("## 🎯 Wickets Timeline")
    
    wickets_data = match_data[match_data['wicket_kind'].notna()].copy()
    
    if len(wickets_data) > 0:
        wickets_info = []
        
        for _, wicket in wickets_data.iterrows():
            wickets_info.append({
                'Over': f"{wicket['over']}.{wicket['ball']}",
                'Innings': wicket['innings'],
                'Team': wicket['batting_team'],
                'Player Out': wicket['player_out'],
                'Wicket Type': wicket['wicket_kind'],
                'Score': wicket['team_runs']
            })
        
        wickets_df = pd.DataFrame(wickets_info)
        st.dataframe(wickets_df, use_container_width=True)
    
    # Over-by-over breakdown
    st.markdown("## 📋 Over-by-Over Breakdown")
    
    innings_select = st.selectbox(
        "Select Innings",
        match_data['innings'].unique(),
        format_func=lambda x: f"Innings {x}"
    )
    
    innings_df = match_data[match_data['innings'] == innings_select].copy()
    
    over_summary = innings_df.groupby('over').agg({
        'runs_total': 'sum',
        'wicket_kind': lambda x: x.notna().sum()
    }).reset_index()
    over_summary.columns = ['Over', 'Runs', 'Wickets']
    over_summary['Summary'] = over_summary.apply(
        lambda x: f"{int(x['Runs'])} runs" + (f", {int(x['Wickets'])} wicket(s)" if x['Wickets'] > 0 else ""),
        axis=1
    )
    
    st.dataframe(over_summary[['Over', 'Runs', 'Wickets', 'Summary']], use_container_width=True)
    
    # commentary
    with st.expander("📝 Ball-by-Ball Commentary"):
        for _, ball in innings_df.iterrows():
            over_ball = f"{ball['over']}.{ball['ball']}"
            batter = ball['batter']
            bowler = ball['bowler']
            runs = ball['runs_total']
            
            commentary = f"**{over_ball}** - {batter} to {bowler}"
            
            if ball['wicket_kind'] is not None and pd.notna(ball['wicket_kind']):
                commentary += f" - **WICKET!** {ball['player_out']} {ball['wicket_kind']}"
            elif runs == 0:
                commentary += " - Dot ball"
            elif runs == 4:
                commentary += " - **FOUR!**"
            elif runs == 6:
                commentary += " - **SIX!**"
            else:
                commentary += f" - {runs} run(s)"
            
            st.markdown(commentary)
    
    # Batting scorecard
    st.markdown("## 🏏 Batting Scorecard")
    
    for innings in match_data['innings'].unique():
        innings_df = match_data[match_data['innings'] == innings]
        batting_team = innings_df['batting_team'].iloc[0]
        
        st.markdown(f"### {batting_team} (Innings {innings})")
        
        batting_stats = innings_df.groupby('batter').agg({
            'runs_batter': 'sum',
            'valid_ball': 'sum',
        }).reset_index()
        
        batting_stats['Strike Rate'] = (batting_stats['runs_batter'] / batting_stats['valid_ball'] * 100).round(1)
        batting_stats.columns = ['Batter', 'Runs', 'Balls', 'Strike Rate']
        batting_stats = batting_stats[batting_stats['Balls'] > 0]
        batting_stats = batting_stats.sort_values('Runs', ascending=False)
        
        st.dataframe(batting_stats, use_container_width=True)
        
        # Total score
        total_runs = innings_df['team_runs'].max()
        total_wickets = innings_df['team_wicket'].max()
        st.markdown(f"**Total: {total_runs}/{total_wickets}**")
        st.markdown("---")
