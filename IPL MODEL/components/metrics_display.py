"""
Reusable metrics display components
"""
import streamlit as st

def display_metric_card(label, value, delta=None, delta_color="normal"):
    """Display a metric card with optional delta"""
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color
    )

def display_kpi_row(metrics_dict):
    """Display a row of KPI metrics"""
    cols = st.columns(len(metrics_dict))
    
    for col, (label, value) in zip(cols, metrics_dict.items()):
        with col:
            st.metric(label=label, value=value)

def display_comparison_metrics(team1_name, team2_name, team1_stats, team2_stats):
    """Display comparison metrics for two teams"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### {team1_name}")
        for key, value in team1_stats.items():
            st.metric(label=key, value=value)
    
    with col2:
        st.markdown("### VS")
    
    with col3:
        st.markdown(f"### {team2_name}")
        for key, value in team2_stats.items():
            st.metric(label=key, value=value)

def display_stat_box(title, value, icon=None):
    """Display a styled stat box"""
    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h3 style="margin: 0; color: white;">{icon if icon else ''} {title}</h3>
            <h1 style="margin: 10px 0 0 0; color: white;">{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_progress_bar(label, value, max_value, format_str=None):
    """Display a progress bar for achievements"""
    st.write(label)
    progress = min(value / max_value, 1.0) if max_value > 0 else 0
    st.progress(progress)
    
    if format_str:
        st.caption(format_str.format(value=value, max=max_value))
    else:
        st.caption(f"{value} / {max_value}")
