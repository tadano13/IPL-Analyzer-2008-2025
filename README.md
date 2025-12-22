# IPL-Analyzer-2008-2025

IPL Analytics & Predictor
This is a project I've been working on to dig into IPL cricket data. I wanted to see if I could find patterns in how teams win, so I built this web app using Python.
It breaks down everything—from player form to how pitch conditions affect the game. I also trained a machine learning model (Random Forest) to predict which team might win based on things like the venue and toss decision. It's not perfect, but it gives some really interesting probabilities!
Tech stack: Python, Streamlit, Pandas, and Scikit-learn.

## Features

### Team Analytics
- Comprehensive team statistics and performance metrics
- Season-by-season performance analysis
- Venue-wise statistics
- Toss decision analysis
- Top performers identification

### Player Analytics
- Detailed individual player statistics
- Batting and bowling performance breakdown
- Career timeline and trends
- Performance against different teams
- Venue-specific analysis

### Match Predictor
- Advanced match outcome predictions using Random Forest
- Team vs team predictions based on venue and toss
- Probability analysis with confidence scores
- Feature importance visualization

### Head-to-Head Analysis
- Direct team comparison
- Historical matchup statistics
- Venue-wise H2H records
- Recent form analysis
- Top performers in H2H matches

### Venue Analysis
- Comprehensive venue statistics
- Pitch behavior insights
- Bat first vs chase analysis
- Team performance at specific venues
- Phase-wise analysis (powerplay, middle overs, death)

### Season Statistics
- Orange Cap race (top run scorers)
- Purple Cap race (top wicket takers)
- Boundary hitters (most fours and sixes)
- Team standings and win percentages
- Best partnerships and highest totals

### Match Simulator
- Replay historical matches ball-by-ball
- Score progression visualization
- Wickets timeline
- Over-by-over breakdown
- Detailed batting and bowling scorecards



## Installation

1. Clone the repository or navigate to the project directory:
```bash
cd "i:\IPL MODEL"
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Data Requirements

**Data Source:** [IPL Dataset (2008-2025)](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025)

The application requires an `IPL.csv` file in the root directory containing ball-by-ball IPL data with the following columns:
- match_id, date, batting_team, bowling_team, venue
- innings, over, ball, batter, bowler
- runs_batter, runs_total, wicket_kind, player_out
- toss_winner, toss_decision, match_won_by
- And other match-related fields

## Project Structure

```
i:/IPL MODEL/
├── app.py                          
├── config.py                      
├── requirements.txt                
├── IPL.csv                       
├── utils/
│   ├── data_loader.py            
│   ├── preprocessor.py            
│   └── metrics.py                
├── models/
│   └── match_predictor.py       
├── pages/
│   ├── Team_Analytics.py
│   ├── Player_Analytics.py
│   ├── Match_Predictor.py
│   ├── Head_to_Head.py
│   ├── Venue_Analysis.py
│   ├── Season_Stats.py
│   ├── Match_Simulator.py

├── components/
│   ├── charts.py                  
│   ├── filters.py                 
│   └── metrics_display.py         
└── .streamlit/
    └── config.toml                
```

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning (Random Forest)

## Features Highlights

- **Ball-by-ball data** from IPL 2008 onwards
- **Machine Learning predictions** for match outcomes
- **Interactive visualizations** using Plotly
- **Advanced statistics** and custom cricket metrics
- **Real-time analysis** with cached data processing
- **Responsive design** with custom styling
- **7 comprehensive feature pages**

## Performance Optimization

- Data caching using Streamlit's `@st.cache_data` decorator
- Efficient data preprocessing and aggregation
- Optimized chart rendering
- Memory-efficient data handling

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available for educational purposes.

## Author

Created by Nishant using Streamlit and Python

---

**Enjoy exploring IPL cricket analytics!** 🏏📊


