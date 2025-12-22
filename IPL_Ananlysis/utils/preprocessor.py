"""
Data preprocessing and feature engineering utilities
"""
import pandas as pd
import streamlit as st

@st.cache_data
def get_team_stats(df, team_name):
    """Calculate comprehensive team statistics"""
    # Batting stats
    batting_df = df[df['batting_team'] == team_name].copy()
    
    # Bowling stats
    bowling_df = df[df['bowling_team'] == team_name].copy()
    
    # Match-level aggregations
    matches_won = df[df['match_won_by'] == team_name]['match_id'].nunique()
    total_matches = df[(df['batting_team'] == team_name) | (df['bowling_team'] == team_name)]['match_id'].nunique()
    
    stats = {
        'total_matches': total_matches,
        'matches_won': matches_won,
        'win_percentage': (matches_won / total_matches * 100) if total_matches > 0 else 0,
        'total_runs_scored': batting_df['runs_total'].sum(),
        'total_wickets_lost': batting_df[batting_df['wicket_kind'].notna()]['wicket_kind'].count(),
        'total_wickets_taken': bowling_df[bowling_df['wicket_kind'].notna()]['wicket_kind'].count(),
        'total_balls_faced': batting_df[batting_df['valid_ball'] == 1]['valid_ball'].count(),
        'total_balls_bowled': bowling_df[bowling_df['valid_ball'] == 1]['valid_ball'].count(),
    }
    
    # Calculate rates
    if stats['total_balls_faced'] > 0:
        stats['batting_strike_rate'] = (stats['total_runs_scored'] / stats['total_balls_faced']) * 100
    else:
        stats['batting_strike_rate'] = 0
    
    if stats['total_balls_bowled'] > 0:
        stats['bowling_economy'] = (stats['total_runs_scored'] / stats['total_balls_bowled']) * 6
    else:
        stats['bowling_economy'] = 0
    
    return stats

@st.cache_data
def get_player_stats(df, player_name):
    """Calculate comprehensive player statistics"""
    # Check if player is primarily a batter or bowler
    batting_df = df[df['batter'] == player_name].copy()
    bowling_df = df[df['bowler'] == player_name].copy()
    
    stats = {}
    
    # Batting stats
    if len(batting_df) > 0:
        stats['batting'] = {
            'innings': batting_df['match_id'].nunique(),
            'runs': batting_df['runs_batter'].sum(),
            'balls': batting_df[batting_df['valid_ball'] == 1]['valid_ball'].count(),
            'fours': batting_df[batting_df['runs_batter'] == 4]['runs_batter'].count(),
            'sixes': batting_df[batting_df['runs_batter'] == 6]['runs_batter'].count(),
            'strike_rate': 0,
            'average': 0,
        }
        
        if stats['batting']['balls'] > 0:
            stats['batting']['strike_rate'] = (stats['batting']['runs'] / stats['batting']['balls']) * 100
        
        # Calculate average (runs per dismissal)
        dismissals = batting_df[batting_df['striker_out'] == True]['striker_out'].count()
        if dismissals > 0:
            stats['batting']['average'] = stats['batting']['runs'] / dismissals
    
    # Bowling stats
    if len(bowling_df) > 0:
        wickets = bowling_df[bowling_df['wicket_kind'].notna()]['wicket_kind'].count()
        runs_conceded = bowling_df['runs_total'].sum()
        balls_bowled = bowling_df[bowling_df['valid_ball'] == 1]['valid_ball'].count()
        
        stats['bowling'] = {
            'innings': bowling_df['match_id'].nunique(),
            'wickets': wickets,
            'runs_conceded': runs_conceded,
            'balls_bowled': balls_bowled,
            'economy': 0,
            'average': 0,
            'strike_rate': 0,
        }
        
        if balls_bowled > 0:
            stats['bowling']['economy'] = (runs_conceded / balls_bowled) * 6
        
        if wickets > 0:
            stats['bowling']['average'] = runs_conceded / wickets
            stats['bowling']['strike_rate'] = balls_bowled / wickets
    
    return stats

@st.cache_data
def get_venue_stats(df, venue_name):
    """Calculate venue-specific statistics"""
    venue_df = df[df['venue'] == venue_name].copy()
    
    # Get innings-wise stats
    innings_1 = venue_df[venue_df['innings'] == 1].groupby('match_id')['team_runs'].max()
    innings_2 = venue_df[venue_df['innings'] == 2].groupby('match_id')['team_runs'].max()
    
    stats = {
        'total_matches': venue_df['match_id'].nunique(),
        'avg_score_innings1': innings_1.mean() if len(innings_1) > 0 else 0,
        'avg_score_innings2': innings_2.mean() if len(innings_2) > 0 else 0,
        'highest_score': venue_df['team_runs'].max(),
        'lowest_score': venue_df.groupby('match_id')['team_runs'].max().min() if len(venue_df) > 0 else 0,
    }
    
    return stats

@st.cache_data
def get_head_to_head(df, team1, team2):
    """Get head-to-head statistics between two teams"""
    h2h_df = df[
        ((df['batting_team'] == team1) & (df['bowling_team'] == team2)) |
        ((df['batting_team'] == team2) & (df['bowling_team'] == team1))
    ].copy()
    
    team1_wins = h2h_df[h2h_df['match_won_by'] == team1]['match_id'].nunique()
    team2_wins = h2h_df[h2h_df['match_won_by'] == team2]['match_id'].nunique()
    total_matches = h2h_df['match_id'].nunique()
    
    return {
        'total_matches': total_matches,
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'team1_win_pct': (team1_wins / total_matches * 100) if total_matches > 0 else 0,
        'team2_win_pct': (team2_wins / total_matches * 100) if total_matches > 0 else 0,
    }

@st.cache_data
def get_season_stats(df, year):
    """Get season-wise statistics"""
    season_df = df[df['year'] == year].copy()
    
    # Top run scorers
    top_batsmen = season_df.groupby('batter').agg({
        'runs_batter': 'sum',
        'match_id': 'nunique'
    }).rename(columns={'runs_batter': 'runs', 'match_id': 'innings'})
    top_batsmen = top_batsmen.sort_values('runs', ascending=False).head(10)
    
    # Top wicket takers
    wickets_df = season_df[season_df['wicket_kind'].notna()].copy()
    top_bowlers = wickets_df.groupby('bowler').agg({
        'wicket_kind': 'count',
        'match_id': 'nunique'
    }).rename(columns={'wicket_kind': 'wickets', 'match_id': 'innings'})
    top_bowlers = top_bowlers.sort_values('wickets', ascending=False).head(10)
    
    return {
        'top_batsmen': top_batsmen,
        'top_bowlers': top_bowlers,
        'total_matches': season_df['match_id'].nunique(),
        'total_runs': season_df['runs_total'].sum(),
        'total_wickets': wickets_df['wicket_kind'].count(),
    }
