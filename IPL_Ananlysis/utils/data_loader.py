"""
Data Loading Module
Author: Nishant
"""
import pandas as pd
import streamlit as st
from pathlib import Path
import config

@st.cache_data(ttl=config.CACHE_TTL)
def load_data():
    """Load the IPL dataset with caching"""
    try:
        # check for zipped data first (github friendly)
        zip_path = Path(__file__).parent.parent / "IPL.zip"
        csv_path = Path(__file__).parent.parent / "IPL.csv"
        
        if zip_path.exists():
            df = pd.read_csv(zip_path, low_memory=False)
        else:
            df = pd.read_csv(csv_path, low_memory=False)
        
        # basic cleaning
        df['date'] = pd.to_datetime(df['date'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def get_teams(df):
    """Get unique list of teams"""
    batting_teams = set(df['batting_team'].dropna().unique())
    bowling_teams = set(df['bowling_team'].dropna().unique())
    return sorted(list(batting_teams | bowling_teams))

@st.cache_data
def get_players(df):
    """Get unique list of players"""
    batters = set(df['batter'].dropna().unique())
    bowlers = set(df['bowler'].dropna().unique())
    return sorted(list(batters | bowlers))

@st.cache_data
def get_venues(df):
    """Get unique list of venues"""
    return sorted(df['venue'].dropna().unique().tolist())

@st.cache_data
def get_seasons(df):
    """Get unique list of seasons/years"""
    return sorted(df['year'].dropna().unique().tolist())

@st.cache_data
def get_matches(df):
    """Get unique match information"""
    match_info = df.groupby('match_id').agg({
        'date': 'first',
        'batting_team': 'first',
        'bowling_team': 'first',
        'venue': 'first',
        'match_won_by': 'first',
        'year': 'first'
    }).reset_index()
    
    return match_info.sort_values('date', ascending=False)
