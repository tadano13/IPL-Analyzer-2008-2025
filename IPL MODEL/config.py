"""
Configuration settings for IPL Analytics Application
"""

# Team color schemes for visualizations
TEAM_COLORS = {
    'Chennai Super Kings': '#FFFF00',
    'Mumbai Indians': '#004BA0',
    'Royal Challengers Bengaluru': '#EC1C24',  # Standardized name
    'Kolkata Knight Riders': '#3A225D',
    'Delhi Capitals': '#004C93',  # Standardized name (was Delhi Daredevils)
    'Sunrisers Hyderabad': '#FF822A',
    'Deccan Chargers': '#6C88C4',
    'Rajasthan Royals': '#254AA5',
    'Punjab Kings': '#ED1B24',  # Standardized name (was Kings XI Punjab)
    'Gujarat Lions': '#E04F16',
    'Rising Pune Supergiant': '#D11D9B',  # Standardized name (singular)
    'Pune Warriors': '#2F9BE3',
    'Kochi Tuskers Kerala': '#8B6914',
    'Lucknow Super Giants': '#3CBBDA',
    'Gujarat Titans': '#1C3F6E',
}

# App settings
APP_TITLE = "🏏 IPL Analytics Hub"
APP_ICON = "🏏"
PAGE_LAYOUT = "wide"

# Chart settings
CHART_HEIGHT = 500
CHART_TEMPLATE = "plotly_white"

# Cache settings (in seconds)
CACHE_TTL = 3600  # 1 hour

# Model settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100

# Display settings
MAX_PLAYERS_DISPLAY = 20
RECENT_MATCHES = 10
