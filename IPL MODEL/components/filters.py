"""
Reusable filter components for Streamlit
"""
import streamlit as st

def season_filter(seasons, key="season"):
    """Season selector filter"""
    return st.selectbox(
        "Select Season",
        options=sorted(seasons, reverse=True),
        key=key
    )

def team_filter(teams, key="team", label="Select Team"):
    """Team selector filter"""
    return st.selectbox(
        label,
        options=teams,
        key=key
    )

def multi_team_filter(teams, key="teams", label="Select Teams"):
    """Multiple team selector filter"""
    return st.multiselect(
        label,
        options=teams,
        default=teams[:2] if len(teams) >= 2 else teams,
        key=key
    )

def player_filter(players, key="player", label="Select Player"):
    """Player selector filter with search"""
    return st.selectbox(
        label,
        options=players,
        key=key
    )

def venue_filter(venues, key="venue"):
    """Venue selector filter"""
    return st.selectbox(
        "Select Venue",
        options=venues,
        key=key
    )

def date_range_filter(min_date, max_date, key="date_range"):
    """Date range selector"""
    return st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=key
    )

def match_type_filter(key="match_type"):
    """Match type filter"""
    return st.selectbox(
        "Match Type",
        options=["All", "League", "Playoff", "Final"],
        key=key
    )
