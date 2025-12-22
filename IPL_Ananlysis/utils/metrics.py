"""
Custom cricket metrics and calculations
"""
import pandas as pd
import numpy as np

def calculate_strike_rate(runs, balls):
    """Calculate strike rate"""
    if balls == 0:
        return 0
    return (runs / balls) * 100

def calculate_economy(runs, balls):
    """Calculate economy rate"""
    if balls == 0:
        return 0
    return (runs / balls) * 6

def calculate_average(runs, dismissals):
    """Calculate batting/bowling average"""
    if dismissals == 0:
        return runs  # Not out
    return runs / dismissals

def calculate_bowling_strike_rate(balls, wickets):
    """Calculate bowling strike rate"""
    if wickets == 0:
        return float('inf')
    return balls / wickets

def calculate_impact_score(runs, balls, wickets, is_batting=True):
    """
    Calculate impact score for a player
    Higher score = higher impact
    """
    if is_batting:
        if balls == 0:
            return 0
        sr = calculate_strike_rate(runs, balls)
        # Impact = runs scored weighted by strike rate
        return runs * (sr / 100)
    else:
        if balls == 0:
            return 0
        economy = calculate_economy(runs, balls)
        # Impact = wickets weighted by economy (lower economy = higher impact)
        wicket_bonus = wickets * 20
        economy_penalty = economy * 2
        return wicket_bonus - economy_penalty

def get_boundary_percentage(fours, sixes, total_runs):
    """Calculate percentage of runs from boundaries"""
    if total_runs == 0:
        return 0
    boundary_runs = (fours * 4) + (sixes * 6)
    return (boundary_runs / total_runs) * 100

def calculate_consistency(scores):
    """
    Calculate consistency score based on coefficient of variation
    Lower CV = higher consistency
    """
    if len(scores) == 0:
        return 0
    
    mean_score = np.mean(scores)
    if mean_score == 0:
        return 0
    
    std_score = np.std(scores)
    cv = (std_score / mean_score) * 100
    
    # Convert to consistency score (inverse of CV, normalized to 0-100)
    consistency = max(0, 100 - cv)
    return consistency

def calculate_form(recent_scores, weights=None):
    """
    Calculate recent form score
    More recent performances weighted higher
    """
    if len(recent_scores) == 0:
        return 0
    
    if weights is None:
        # Default weights: more recent = higher weight
        weights = np.linspace(0.5, 1.5, len(recent_scores))
    
    weighted_avg = np.average(recent_scores, weights=weights)
    return weighted_avg
