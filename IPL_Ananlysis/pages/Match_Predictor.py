"""
Match Predictor Page
"""
import streamlit as st
from utils.data_loader import load_data, get_teams, get_venues
from models.match_predictor import train_match_predictor, predict_match
from components.charts import create_gauge_chart
import plotly.graph_objects as go

st.set_page_config(page_title="Match Predictor", page_icon="🎯", layout="wide")

st.title("🎯 Match Outcome Predictor")
st.markdown("Advanced match prediction using machine learning")

# loading data
df = load_data()
if df is None:
    st.error("Failed to load data")
    st.stop()

teams = get_teams(df)
venues = get_venues(df)

# model training
with st.spinner("Training prediction model..."):
    model, encoders, features = train_match_predictor(df)

if model is None:
    st.error("Failed to train prediction model. Need more data.")
    st.stop()

st.success("✅ Prediction model ready!")

# input fields
st.markdown("## 🏏 Match Details")

col1, col2, col3 = st.columns(3)

with col1:
    team1 = st.selectbox("Team 1 (Batting First)", teams, key="team1_pred")

with col2:
    team2_options = [t for t in teams if t != team1]
    team2 = st.selectbox("Team 2 (Bowling First)", team2_options, key="team2_pred")

with col3:
    venue = st.selectbox("Venue", venues, key="venue_pred")

col4, col5 = st.columns(2)

with col4:
    toss_winner = st.selectbox("Toss Winner", [team1, team2], key="toss_winner")

with col5:
    toss_decision = st.selectbox("Toss Decision", ["bat", "field"], key="toss_decision")

# prediction logic
if st.button("🔮 Predict Match Outcome", type="primary", use_container_width=True):
    with st.spinner("Predicting match outcome..."):
        try:
            prediction = predict_match(model, encoders, team1, team2, venue, toss_winner, toss_decision)
            
            if 'error' in prediction:
                st.error(f"Prediction error: {prediction['error']}")
            else:
                st.markdown("---")
                st.markdown("## 🏆 Prediction Results")
                
                # Winner announcement
                st.markdown(f"""
                    <div style="
                        text-align: center;
                        padding: 30px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        margin: 20px 0;
                    ">
                        <h2 style="color: white; margin: 0;">Predicted Winner</h2>
                        <h1 style="color: #FFD700; margin: 10px 0; font-size: 3em;">🏆 {prediction['winner']}</h1>
                        <p style="color: white; font-size: 1.2em;">Confidence: {prediction['confidence']:.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Probability breakdown
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### {team1}")
                    fig1 = create_gauge_chart(
                        prediction['team1_probability'],
                        f"{team1} Win Probability",
                        max_value=100
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {team2}")
                    fig2 = create_gauge_chart(
                        prediction['team2_probability'],
                        f"{team2} Win Probability",
                        max_value=100
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Visual comparison
                st.markdown("### Win Probability Comparison")
                fig = go.Figure(data=[
                    go.Bar(
                        name='Win Probability %',
                        x=[team1, team2],
                        y=[prediction['team1_probability'], prediction['team2_probability']],
                        marker_color=['#667eea', '#764ba2'],
                        text=[f"{prediction['team1_probability']:.1f}%", 
                              f"{prediction['team2_probability']:.1f}%"],
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Win Probability Comparison",
                    yaxis_title="Probability (%)",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Disclaimer
                st.info("""
                ℹ️ **Note**: This prediction is based on historical data and machine learning models. 
                Actual match outcomes can vary based on many factors including current form, player availability, 
                and match conditions.
                """)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# about model
with st.expander("ℹ️ About the Prediction Model"):
    st.markdown("""
    ### How it works:
    
    This prediction model uses **Random Forest Classification** trained on historical IPL match data.
    
    **Features considered:**
    - Team 1 (Batting first)
    - Team 2 (Bowling first)
    - Venue
    - Toss winner
    - Toss decision
    
    **Model Accuracy:**
    The model has been trained on thousands of historical IPL matches to learn patterns and 
    predict outcomes based on the input parameters.
    
    **Limitations:**
    - Does not consider current player form
    - Does not account for injuries or team changes
    - Historical data may not reflect current team strength
    """)
