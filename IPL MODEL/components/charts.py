"""
Reusable chart components using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config

def create_bar_chart(data, x, y, title, color=None, orientation='v'):
    """Create a styled bar chart"""
    fig = px.bar(
        data, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        color_discrete_map=config.TEAM_COLORS if color else None,
        orientation=orientation,
        template=config.CHART_TEMPLATE
    )
    
    fig.update_layout(
        height=config.CHART_HEIGHT,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_line_chart(data, x, y, title, color=None):
    """Create a styled line chart"""
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        color_discrete_map=config.TEAM_COLORS if color else None,
        markers=True,
        template=config.CHART_TEMPLATE
    )
    
    fig.update_layout(
        height=config.CHART_HEIGHT,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_pie_chart(values, names, title):
    """Create a styled pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=names,
        values=values,
        hole=0.3,
        marker=dict(colors=[config.TEAM_COLORS.get(name, '#808080') for name in names])
    )])
    
    fig.update_layout(
        title=title,
        height=config.CHART_HEIGHT,
        template=config.CHART_TEMPLATE
    )
    
    return fig

def create_scatter_plot(data, x, y, title, color=None, size=None):
    """Create a styled scatter plot"""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        color_discrete_map=config.TEAM_COLORS if color else None,
        template=config.CHART_TEMPLATE
    )
    
    fig.update_layout(
        height=config.CHART_HEIGHT,
        showlegend=True
    )
    
    return fig

def create_heatmap(data, title, x_label=None, y_label=None):
    """Create a styled heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='RdYlGn',
        text=data.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
    ))
    
    fig.update_layout(
        title=title,
        height=config.CHART_HEIGHT,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=config.CHART_TEMPLATE
    )
    
    return fig

def create_radar_chart(categories, values1, values2, name1, name2):
    """Create a radar chart for comparison"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values1,
        theta=categories,
        fill='toself',
        name=name1
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values2,
        theta=categories,
        fill='toself',
        name=name2
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(values1), max(values2)) * 1.1]
            )
        ),
        showlegend=True,
        height=config.CHART_HEIGHT,
        template=config.CHART_TEMPLATE
    )
    
    return fig

def create_gauge_chart(value, title, max_value=100):
    """Create a gauge chart for metrics"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "lightgray"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "gray"},
                {'range': [max_value * 0.66, max_value], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        template=config.CHART_TEMPLATE
    )
    
    return fig
