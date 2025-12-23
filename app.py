"""
IPL Analytics Hub - Main Application
Author: Nishant
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_teams, get_players, get_venues, get_seasons
from components.metrics_display import display_kpi_row, display_stat_box
import config

# page settings
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# styling stuff
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .feature-box {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .stMetric {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# getting the data
@st.cache_data
def get_quick_stats(df):
    """calc quick stats"""
    return {
        'Total Matches': df['match_id'].nunique(),
        'Total Players': len(set(df['batter'].unique()) | set(df['bowler'].unique())),
        'Total Teams': len(get_teams(df)),
        'Total Seasons': len(get_seasons(df)),
        'Total Runs': int(df['runs_total'].sum()),
        'Total Wickets': int(df[df['wicket_kind'].notna()]['wicket_kind'].count()),
    }

# Main content
def main():
    # Hero section
    st.markdown('<h1 class="main-header">🏏 IPL Analytics Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Comprehensive Cricket Analytics & Predictions Platform</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading IPL data..."):
        df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check if IPL.csv exists in the correct location.")
        return
    
    st.success(f"✅ Loaded {len(df):,} ball-by-ball records from IPL history!")
    
    # Quick stats
    st.markdown("---")
    st.markdown("## 📊 Quick Statistics")
    
    stats = get_quick_stats(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        display_stat_box("Total Matches", f"{stats['Total Matches']:,}", "🏏")
    with col2:
        display_stat_box("Total Players", f"{stats['Total Players']:,}", "👤")
    with col3:
        display_stat_box("Total Teams", f"{stats['Total Teams']}", "🏆")
    
    st.markdown("")
    col4, col5, col6 = st.columns(3)
    with col4:
        display_stat_box("Seasons Covered", f"{stats['Total Seasons']}", "📅")
    with col5:
        display_stat_box("Total Runs", f"{stats['Total Runs']:,}", "🎯")
    with col6:
        display_stat_box("Total Wickets", f"{stats['Total Wickets']:,}", "🎳")
    
    # Features overview
    st.markdown("---")
    st.markdown("## 🎯 Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🏏 Team Analytics</h3>
            <p>Comprehensive team statistics, performance trends, and venue analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>👤 Player Analytics</h3>
            <p>Detailed player statistics, career timelines, and performance metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🎯 Match Predictor</h3>
            <p>Advanced match outcome predictions using machine learning</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>⚔️ Head-to-Head</h3>
            <p>Compare teams and analyze historical matchups</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🏟️ Venue Analysis</h3>
            <p>Venue-specific statistics and pitch behavior insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Season Statistics</h3>
            <p>Season-wise analysis with top performers and highlights</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🎮 Match Simulator</h3>
            <p>Replay historical matches ball-by-ball with visualizations</p>
        </div>
        """, unsafe_allow_html=True)
        

    
    # How to use
    st.markdown("---")
    st.markdown("## 📖 How to Use")
    st.info("""
    👈 **Navigate using the sidebar** to access different features:
    
    - **Team Analytics**: Analyze team performance across seasons and venues
    - **Player Analytics**: Deep dive into individual player statistics
    - **Match Predictor**: Predict match outcomes with AI
    - **Head-to-Head**: Compare two teams directly
    - **Venue Analysis**: Understand venue characteristics
    - **Season Stats**: Explore season-wise records
    - **Match Simulator**: Watch historical matches unfold

    """)
    
    # About
    st.markdown("---")
    st.markdown("## ℹ️ About This App")
    st.markdown("""
    This comprehensive IPL Analytics platform provides:
    - **Ball-by-ball data** from IPL 2008 onwards
    - **Machine Learning predictions** for match outcomes
    - **Interactive visualizations** using Plotly
    - **Advanced statistics** and custom metrics
    - **Real-time analysis** with cached data processing
    
    Built using **Streamlit**, **Pandas**, **Plotly**, and **Scikit-learn**.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>IPL Analytics Hub | Data-Driven Cricket Insights</p>
            <p>🏏 Powered by Streamlit & Python</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
