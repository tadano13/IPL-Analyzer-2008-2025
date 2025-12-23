"""
Match Prediction Logic
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import config

@st.cache_resource
def train_match_predictor(df):
    """Train prediction model"""
    try:
        # getting match data
        match_data = df.groupby('match_id').agg({
            'batting_team': 'first',
            'bowling_team': 'first',
            'venue': 'first',
            'toss_winner': 'first',
            'toss_decision': 'first',
            'match_won_by': 'first',
        }).reset_index()
        
        # remove missing stuff
        match_data = match_data.dropna()
        
        if len(match_data) < 50:  # Need minimum data
            return None, None, None
        
        # encoding vars
        le_team1 = LabelEncoder()
        le_team2 = LabelEncoder()
        le_venue = LabelEncoder()
        le_toss_winner = LabelEncoder()
        le_toss_decision = LabelEncoder()
        
        match_data['team1_encoded'] = le_team1.fit_transform(match_data['batting_team'])
        match_data['team2_encoded'] = le_team2.fit_transform(match_data['bowling_team'])
        match_data['venue_encoded'] = le_venue.fit_transform(match_data['venue'])
        match_data['toss_winner_encoded'] = le_toss_winner.fit_transform(match_data['toss_winner'])
        match_data['toss_decision_encoded'] = le_toss_decision.fit_transform(match_data['toss_decision'])
        
        # Features and target
        features = ['team1_encoded', 'team2_encoded', 'venue_encoded', 
                   'toss_winner_encoded', 'toss_decision_encoded']
        X = match_data[features]
        y = (match_data['match_won_by'] == match_data['batting_team']).astype(int)
        
        # training it
        model = RandomForestClassifier(
            n_estimators=config.N_ESTIMATORS,
            random_state=config.RANDOM_STATE,
            max_depth=10
        )
        model.fit(X, y)
        
        encoders = {
            'team1': le_team1,
            'team2': le_team2,
            'venue': le_venue,
            'toss_winner': le_toss_winner,
            'toss_decision': le_toss_decision
        }
        
        return model, encoders, features
    
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return None, None, None

def predict_match(model, encoders, team1, team2, venue, toss_winner, toss_decision):
    """Predict match outcome"""
    try:
        # Encode inputs
        team1_enc = encoders['team1'].transform([team1])[0]
        team2_enc = encoders['team2'].transform([team2])[0]
        venue_enc = encoders['venue'].transform([venue])[0]
        toss_winner_enc = encoders['toss_winner'].transform([toss_winner])[0]
        toss_decision_enc = encoders['toss_decision'].transform([toss_decision])[0]
        
        # Make prediction
        X = np.array([[team1_enc, team2_enc, venue_enc, toss_winner_enc, toss_decision_enc]])
        
        prediction_proba = model.predict_proba(X)[0]
        prediction = model.predict(X)[0]
        
        return {
            'winner': team1 if prediction == 1 else team2,
            'team1_probability': prediction_proba[1] * 100,
            'team2_probability': prediction_proba[0] * 100,
            'confidence': max(prediction_proba) * 100
        }
    
    except Exception as e:
        return {
            'winner': 'Error',
            'team1_probability': 50,
            'team2_probability': 50,
            'confidence': 0,
            'error': str(e)
        }
