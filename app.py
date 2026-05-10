import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

from data_generator import generate_synthetic_data, generate_customer_data
from utils import (
    format_currency, format_percentage, format_number,
    calculate_kpis, get_ai_insights, create_alert_list,
    generate_report_data, color_palette
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Raymond Retail Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - LUXURY/REFINED AESTHETIC
# ============================================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --primary: {color_palette['primary']};
    --secondary: {color_palette['secondary']};
    --accent: {color_palette['accent']};
    --success: {color_palette['success']};
    --warning: {color_palette['warning']};
    --danger: {color_palette['danger']};
    --dark: {color_palette['dark']};
    --light: {color_palette['light']};
}}

* {{
    font-family: 'Inter', sans-serif;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

body {{
    background-color: {color_palette['dark']};
    color: {color_palette['light']};
}}

.main {{
    background-color: {color_palette['dark']};
    padding: 2rem;
}}

[data-testid="stMetricLabel"] {{
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(255, 255, 255, 0.6);
}}

[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: {color_palette['accent']};
    letter-spacing: -0.02em;
}}

.metric-card {{
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    border-color: {color_palette['accent']};
    box-shadow: 0 8px 32px rgba(255, 215, 0, 0.1);
}}

.header-title {{
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, {color_palette['accent']} 0%, {color_palette['secondary']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}}

.subtitle {{
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 2rem;
}}

.divider {{
    height: 1px;
    background: linear-gradient(90deg, rgba(255,215,0,0) 0%, rgba(255,215,0,0.3) 50%, rgba(255,215,0,0) 100%);
    margin: 2rem 0;
}}

.filter-container {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}}

.insight-box {{
    background: rgba(255, 215, 0, 0.05);
    border-left: 4px solid {color_palette['accent']};
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
}}

.alert-danger {{
    background: rgba(220, 53, 69, 0.1);
    border-left: 4px solid {color_palette['danger']};
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
}}

.alert-warning {{
    background: rgba(255, 193, 7, 0.1);
    border-left: 4px solid {color_palette['warning']};
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.2) 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}}

.stSelectbox [data-baseweb="select__control"] {{
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
    color: white;
}}

.stDateInput [data-baseweb="input"] {{
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
}}

.stButton > button {{
    background: linear-gradient(135deg, {color_palette['accent']} 0%, {color_palette['secondary']} 100%);
    color: {color_palette['dark']};
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.85rem;
}}

.stButton > button:hover {{
    box-shadow: 0 8px 24px rgba(255, 215, 0, 0.3);
}}

.stTabs [data-baseweb="tab-list"] {{
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.stTabs [aria-selected="true"] {{
    border-bottom: 2px solid {color_palette['accent']};
}}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE & DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Generate or load synthetic data"""
    sales_data = generate_synthetic_data()
    customer_data = generate_customer_data()
    return sales_data, customer_data

@st.cache_data
def prepare_forecast_data(df):
    """Prepare data for Prophet forecasting"""
    forecast_data = df.groupby('date')['sales'].sum().reset_index()
    forecast_data.columns = ['ds', 'y']
    return forecast_data

# Load data
sales_df, customer_df = load_data()

# ============================================================================
# SIDEBAR - FILTERS & NAVIGATION
# ============================================================================

st.sidebar.markdown(f"<div class='header-title' style='font-size:1.8rem; margin-bottom:2rem;'>🏪 RAYMOND</div>", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Sales Analytics", "Inventory Management", "Customer Insights", "Forecasting", "Reports"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Date Range Filter
st.sidebar.markdown("**Date Range**")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "From",
        value=sales_df['date'].min(),
        key="start_date",
        label_visibility="collapsed"
    )
with col2:
    end_date = st.date_input(
        "To",
        value=sales_df['date'].max(),
        key="end_date",
        label_visibility="collapsed"
    )

# Store Filter
st.sidebar.markdown("**Stores**")
all_stores = sorted(sales_df['store_name'].unique())
selected_stores = st.sidebar.multiselect(
    "Select Stores",
    all_stores,
    default=all_stores,
    label_visibility="collapsed",
    max_selections=10
)

# Category Filter
st.sidebar.markdown("**Categories**")
all_categories = sorted(sales_df['category'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    all_categories,
    default=all_categories,
    label_visibility="collapsed"
)

# Filter data
filtered_df = sales_df[
    (sales_df['date'] >= pd.to_datetime(start_date)) &
    (sales_df['date'] <= pd.to_datetime(end_date)) &
    (sales_df['store_name'].isin(selected_stores)) &
    (sales_df['category'].isin(selected_categories))
].copy()

# ============================================================================
# HELPER FUNCTION FOR KPI DISPLAY
# ============================================================================

def display_kpi_card(col, metric_name, value, change, icon="📈"):
    """Display a styled KPI card"""
    change_color = "🟢" if change >= 0 else "🔴"
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: rgba(255,255,255,0.6); margin-bottom: 0.5rem;'>
                {icon} {metric_name}
            </div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #FFD700; margin-bottom: 0.5rem;'>
                {value}
            </div>
            <div style='font-size: 0.9rem; color: rgba(255,255,255,0.6);'>
                {change_color} {abs(change):.1f}% from last period
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 1: OVERVIEW (EXECUTIVE DASHBOARD)
# ============================================================================

if page == "Overview":
    st.markdown(f"<div class='header-title'>Executive Overview</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Real-time KPIs & Performance Metrics</div>", unsafe_allow_html=True)
    
    # Calculate KPIs
    kpis = calculate_kpis(filtered_df, sales_df)
    
    # KPI Row 1
    col1, col2, col3, col4, col5 = st.columns(5)
    
    display_kpi_card(col1, "Total Sales", format_currency(kpis['total_sales']), kpis['sales_change'], "💰")
    display_kpi_card(col2, "Total Profit", format_currency(kpis['total_profit']), kpis['profit_change'], "📊")
    display_kpi_card(col3, "Avg Order Value", format_currency(kpis['avg_order_value']), kpis['aov_change'], "🛍️")
    display_kpi_card(col4, "Store Footfall", format_number(kpis['total_footfall']), kpis['footfall_change'], "👥")
    display_kpi_card(col5, "Inventory Turnover", f"{kpis['inventory_turnover']:.2f}x", 5.2, "🔄")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sales Trend**")
        daily_sales = filtered_df.groupby('date').agg({
            'sales': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['sales'],
            fill='tozeroy',
            name='Sales',
            line=dict(color='#FFD700', width=3),
            fillcolor='rgba(255, 215, 0, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['profit'],
            name='Profit',
            line=dict(color='#00D9FF', width=2, dash='dash'),
        ))
        fig.update_layout(
            template='plotly_dark',
            height=350,
            hovermode='x unified',
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.3)')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("**Sales by Category**")
        category_sales = filtered_df.groupby('category')['sales'].sum().sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=category_sales.index,
                x=category_sales.values,
                orientation='h',
                marker=dict(
                    color=category_sales.values,
                    colorscale='Viridis',
                    showscale=False
                ),
                text=category_sales.values.apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            height=350,
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 10 Stores by Sales**")
        store_sales = filtered_df.groupby('store_name')['sales'].sum().nlargest(10).sort_values()
        
        fig = go.Figure(data=[
            go.Bar(
                y=store_sales.index,
                x=store_sales.values,
                orientation='h',
                marker=dict(color='#FFD700'),
                text=store_sales.values.apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("**Profit Margin by Category**")
        margin_data = filtered_df.groupby('category').apply(
            lambda x: (x['profit'].sum() / x['sales'].sum() * 100) if x['sales'].sum() > 0 else 0
        ).sort_values()
        
        fig = go.Figure(data=[
            go.Bar(
                y=margin_data.index,
                x=margin_data.values,
                orientation='h',
                marker=dict(
                    color=margin_data.values,
                    colorscale=['#DC3545', '#FFC107', '#28A745'],
                    showscale=False
                ),
                text=margin_data.values.apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # AI Insights
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("**🤖 AI-Driven Business Insights**")
    
    insights = get_ai_insights(filtered_df, kpis)
    for i, insight in enumerate(insights):
        if i % 2 == 0:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

# ============================================================================
# PAGE 2: SALES ANALYTICS
# ============================================================================

elif page == "Sales Analytics":
    st.markdown(f"<div class='header-title'>Sales Analytics</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Detailed sales performance & benchmarking</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Trend Analysis", "Store Comparison", "Seasonal Analysis", "Campaign ROI"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Daily Sales with Moving Average**")
            daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
            daily_sales['MA_7'] = daily_sales['sales'].rolling(window=7).mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['sales'],
                name='Daily Sales',
                line=dict(color='rgba(255, 215, 0, 0.5)', width=1),
                fillcolor='rgba(255, 215, 0, 0.1)',
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['MA_7'],
                name='7-Day MA',
                line=dict(color='#FFD700', width=3),
                mode='lines'
            ))
            fig.update_layout(
                template='plotly_dark',
                height=450,
                hovermode='x unified',
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("**Sales Distribution by Store**")
            store_stats = filtered_df.groupby('store_name')['sales'].agg(['mean', 'std']).reset_index()
            
            fig = go.Figure(data=[
                go.Box(
                    y=filtered_df.groupby('store_name')['sales'].apply(list),
                    name='Sales Distribution',
                    marker_color='#FFD700',
                    boxmean='sd'
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=450,
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown("**Store Performance Matrix**")
        
        store_metrics = filtered_df.groupby('store_name').agg({
            'sales': 'sum',
            'profit': 'sum',
            'quantity': 'sum',
            'footfall': 'sum'
        }).reset_index()
        store_metrics['profit_margin'] = (store_metrics['profit'] / store_metrics['sales'] * 100).round(2)
        store_metrics['aov'] = (store_metrics['sales'] / store_metrics['quantity']).round(2)
        store_metrics = store_metrics.sort_values('sales', ascending=False)
        
        fig = go.Figure(data=[
            go.Scatter(
                x=store_metrics['sales'],
                y=store_metrics['profit_margin'],
                mode='markers+text',
                marker=dict(
                    size=store_metrics['footfall'] / store_metrics['footfall'].max() * 40,
                    color=store_metrics['profit'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Profit ($)"),
                    line=dict(width=1, color='rgba(255,255,255,0.3)')
                ),
                text=store_metrics['store_name'],
                textposition='top center',
                textfont=dict(size=9)
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            height=500,
            xaxis_title='Total Sales ($)',
            yaxis_title='Profit Margin (%)',
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Store Metrics Table
        st.markdown("**Detailed Store Metrics**")
        display_df = store_metrics.copy()
        display_df['sales'] = display_df['sales'].apply(lambda x: f'${x:,.0f}')
        display_df['profit'] = display_df['profit'].apply(lambda x: f'${x:,.0f}')
        display_df['aov'] = display_df['aov'].apply(lambda x: f'${x:.2f}')
        display_df['profit_margin'] = display_df['profit_margin'].apply(lambda x: f'{x:.1f}%')
        display_df = display_df[['store_name', 'sales', 'profit', 'profit_margin', 'aov', 'footfall']]
        display_df.columns = ['Store', 'Sales', 'Profit', 'Margin', 'AOV', 'Footfall']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("**Seasonal Demand Pattern**")
        
        filtered_df['month'] = filtered_df['date'].dt.to_period('M').astype(str)
        monthly_sales = filtered_df.groupby('month')['sales'].sum().reset_index()
        monthly_sales['sales_norm'] = (monthly_sales['sales'] - monthly_sales['sales'].min()) / (monthly_sales['sales'].max() - monthly_sales['sales'].min()) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_sales['month'],
            y=monthly_sales['sales'],
            marker=dict(
                color=monthly_sales['sales_norm'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Sales")
            ),
            text=monthly_sales['sales'].apply(lambda x: f'${x/1000:.1f}K'),
            textposition='outside'
        ))
        fig.update_layout(
            template='plotly_dark',
            height=450,
            xaxis_title='Month',
            yaxis_title='Sales ($)',
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab4:
        st.markdown("**Campaign Performance & ROI**")
        
        # Generate campaign data
        campaign_df = filtered_df.groupby('promotion_type').agg({
            'sales': 'sum',
            'profit': 'sum',
            'quantity': 'sum'
        }).reset_index()
        campaign_df['roi'] = (campaign_df['profit'] / campaign_df['sales'] * 100).round(2)
        campaign_df = campaign_df[campaign_df['promotion_type'] != 'None'].sort_values('roi', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=campaign_df['promotion_type'],
                    y=campaign_df['roi'],
                    marker=dict(
                        color=campaign_df['roi'],
                        colorscale='RdYlGn',
                        showscale=False
                    ),
                    text=campaign_df['roi'].apply(lambda x: f'{x:.1f}%'),
                    textposition='outside'
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=400,
                title='ROI by Campaign Type',
                xaxis_title='Campaign Type',
                yaxis_title='ROI (%)',
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            fig = go.Figure(data=[
                go.Pie(
                    labels=campaign_df['promotion_type'],
                    values=campaign_df['sales'],
                    marker=dict(
                        colors=['#FFD700', '#00D9FF', '#FF6B9D', '#A78BFA'],
                        line=dict(width=2, color='rgba(0,0,0,0.3)')
                    )
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=400,
                title='Sales by Campaign Type',
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# PAGE 3: INVENTORY MANAGEMENT
# ============================================================================

elif page == "Inventory Management":
    st.markdown(f"<div class='header-title'>Inventory Management</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Stock levels, turnover, and alerts</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Inventory Status", "Turnover Analysis", "Alerts & Recommendations"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Current Inventory Levels by Category**")
            inventory_by_cat = filtered_df.groupby('category').agg({
                'stock': 'sum',
                'sales': 'sum',
                'quantity': 'sum'
            }).reset_index()
            inventory_by_cat['turnover_ratio'] = inventory_by_cat['quantity'] / inventory_by_cat['stock'].replace(0, 1)
            
            fig = go.Figure(data=[
                go.Bar(
                    name='Stock Level',
                    x=inventory_by_cat['category'],
                    y=inventory_by_cat['stock'],
                    marker=dict(color='#00D9FF'),
                    yaxis='y'
                ),
                go.Scatter(
                    name='Turnover Ratio',
                    x=inventory_by_cat['category'],
                    y=inventory_by_cat['turnover_ratio'],
                    marker=dict(color='#FFD700', size=10),
                    yaxis='y2'
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=450,
                xaxis_title='Category',
                yaxis=dict(title='Stock Level', side='left'),
                yaxis2=dict(title='Turnover Ratio', overlaying='y', side='right'),
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("**Inventory KPIs**")
            total_stock = filtered_df['stock'].sum()
            total_stock_value = (filtered_df['stock'] * filtered_df['price']).sum()
            avg_turnover = (filtered_df['quantity'].sum() / filtered_df['stock'].sum()) if filtered_df['stock'].sum() > 0 else 0
            
            st.metric("Total Stock Units", format_number(int(total_stock)))
            st.metric("Stock Value", format_currency(total_stock_value))
            st.metric("Avg Turnover", f"{avg_turnover:.2f}x")
    
    with tab2:
        st.markdown("**Inventory Turnover by Store**")
        
        store_inventory = filtered_df.groupby('store_name').agg({
            'stock': 'sum',
            'quantity': 'sum',
            'sales': 'sum',
            'price': 'mean'
        }).reset_index()
        store_inventory['turnover'] = store_inventory['quantity'] / store_inventory['stock'].replace(0, 1)
        store_inventory = store_inventory.sort_values('turnover', ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=store_inventory['store_name'],
                y=store_inventory['turnover'],
                marker=dict(
                    color=store_inventory['turnover'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Turnover")
                ),
                text=store_inventory['turnover'].apply(lambda x: f'{x:.2f}x'),
                textposition='outside'
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            height=450,
            xaxis_title='Store',
            yaxis_title='Turnover Ratio',
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.markdown("**Inventory Alerts**")
        
        alerts = create_alert_list(filtered_df)
        
        if alerts:
            for alert_type, alert_msg, severity in alerts:
                if severity == 'critical':
                    st.markdown(f"<div class='alert-danger'>🚨 {alert_msg}</div>", unsafe_allow_html=True)
                elif severity == 'warning':
                    st.markdown(f"<div class='alert-warning'>⚠️ {alert_msg}</div>", unsafe_allow_html=True)
                else:
                    st.info(f"ℹ️ {alert_msg}")
        else:
            st.success("✅ All inventory levels are healthy!")
        
        st.markdown("**Smart Recommendations**")
        st.markdown("""
        - **Overstock Management**: Categories with turnover < 1.5x should be discounted or promoted
        - **Stockout Prevention**: Maintain 2-3x seasonal demand buffer during peak seasons
        - **ABC Analysis**: Focus on A-items (80% revenue, 20% inventory) for active management
        - **Reorder Point**: Set reorder at 30 days of average usage
        """)

# ============================================================================
# PAGE 4: CUSTOMER INSIGHTS
# ============================================================================

elif page == "Customer Insights":
    st.markdown(f"<div class='header-title'>Customer Insights</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Segmentation, behavior, and lifetime value</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Segmentation", "Behavior Analysis", "Lifetime Value"])
    
    with tab1:
        st.markdown("**Customer Segmentation (K-Means Clustering)**")
        
        # Prepare customer features
        customer_features = customer_df[['total_spend', 'num_purchases', 'avg_order_value', 'days_since_purchase']].copy()
        
        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(customer_features)
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        customer_df['segment'] = kmeans.fit_predict(features_scaled)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter_3d(
                customer_df,
                x='total_spend',
                y='num_purchases',
                z='avg_order_value',
                color='segment',
                title='Customer Segments (3D View)',
                color_continuous_scale='Viridis',
                labels={
                    'total_spend': 'Total Spend ($)',
                    'num_purchases': 'Purchases',
                    'avg_order_value': 'Avg Order Value ($)'
                }
            )
            fig.update_layout(
                template='plotly_dark',
                height=500,
                margin=dict(l=40, r=40, t=60, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("**Segment Profiles**")
            
            segment_summary = customer_df.groupby('segment').agg({
                'customer_id': 'count',
                'total_spend': ['mean', 'sum'],
                'num_purchases': 'mean',
                'avg_order_value': 'mean',
                'days_since_purchase': 'mean'
            }).round(2)
            
            # Create segment names
            segment_names = {
                0: "Premium Buyers",
                1: "Frequent Shoppers",
                2: "Dormant Customers",
                3: "New Customers"
            }
            
            for seg in sorted(customer_df['segment'].unique()):
                seg_size = len(customer_df[customer_df['segment'] == seg])
                seg_value = customer_df[customer_df['segment'] == seg]['total_spend'].mean()
                st.markdown(f"""
                **{segment_names.get(seg, f'Segment {seg}')}**
                - Size: {seg_size} customers
                - Avg Spend: ${seg_value:,.0f}
                """)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Purchase Frequency Distribution**")
            fig = go.Figure(data=[
                go.Histogram(
                    x=customer_df['num_purchases'],
                    nbinsx=20,
                    marker=dict(color='#FFD700', line=dict(width=1, color='rgba(255,255,255,0.2)'))
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=400,
                xaxis_title='Number of Purchases',
                yaxis_title='Customer Count',
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("**Average Order Value Distribution**")
            fig = go.Figure(data=[
                go.Histogram(
                    x=customer_df['avg_order_value'],
                    nbinsx=25,
                    marker=dict(color='#00D9FF', line=dict(width=1, color='rgba(255,255,255,0.2)'))
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=400,
                xaxis_title='Avg Order Value ($)',
                yaxis_title='Customer Count',
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.markdown("**Customer Lifetime Value (CLV) Analysis**")
        
        customer_df['clv_segment'] = pd.cut(
            customer_df['total_spend'],
            bins=4,
            labels=['Low', 'Medium', 'High', 'VIP']
        )
        
        clv_summary = customer_df.groupby('clv_segment').agg({
            'customer_id': 'count',
            'total_spend': ['mean', 'sum'],
            'num_purchases': 'mean'
        }).round(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Pie(
                    labels=customer_df['clv_segment'].value_counts().index,
                    values=customer_df['clv_segment'].value_counts().values,
                    marker=dict(colors=['#FF6B9D', '#A78BFA', '#00D9FF', '#FFD700']),
                    textinfo='label+percent'
                )
            ])
            fig.update_layout(
                template='plotly_dark',
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                title='Customer Distribution by CLV'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("**CLV by Segment**")
            clv_by_seg = customer_df.groupby('clv_segment')['total_spend'].agg(['count', 'mean', 'sum']).reset_index()
            clv_by_seg.columns = ['Segment', 'Count', 'Avg Spend', 'Total Revenue']
            clv_by_seg['Avg Spend'] = clv_by_seg['Avg Spend'].apply(lambda x: f'${x:,.0f}')
            clv_by_seg['Total Revenue'] = clv_by_seg['Total Revenue'].apply(lambda x: f'${x:,.0f}')
            
            st.dataframe(clv_by_seg, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE 5: FORECASTING
# ============================================================================

elif page == "Forecasting":
    st.markdown(f"<div class='header-title'>Sales Forecasting</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Predictive models & trend analysis</div>", unsafe_allow_html=True)
    
    # Prepare forecast data
    forecast_data = prepare_forecast_data(filtered_df)
    
    if len(forecast_data) > 20:
        with st.spinner("⏳ Training Prophet model..."):
            # Train Prophet
            model = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=True, interval_width=0.95)
            model.add_seasonality(name='monthly', period=30, fourier_order=5)
            model.fit(forecast_data)
            
            # Make forecast
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)
            
            # Plot forecast
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['y'],
                name='Historical Sales',
                mode='lines',
                line=dict(color='#FFD700', width=2),
                fill='tozeroy',
                fillcolor='rgba(255, 215, 0, 0.1)'
            ))
            
            # Forecast
            forecast_future = forecast[forecast['ds'] > forecast_data['ds'].max()]
            fig.add_trace(go.Scatter(
                x=forecast_future['ds'],
                y=forecast_future['yhat'],
                name='Forecast',
                mode='lines',
                line=dict(color='#00D9FF', width=2, dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_future['ds'],
                y=forecast_future['yhat_upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,217,255,0)',
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=forecast_future['ds'],
                y=forecast_future['yhat_lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,217,255,0)',
                name='95% Confidence',
                fillcolor='rgba(0, 217, 255, 0.2)'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                title='30-Day Sales Forecast',
                xaxis_title='Date',
                yaxis_title='Sales ($)',
                margin=dict(l=40, r=40, t=60, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='rgba(255,255,255,0.8)'),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Forecast metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_forecast = forecast_future['yhat'].mean()
                st.metric("Avg Daily Forecast", format_currency(avg_forecast))
            
            with col2:
                total_30d = forecast_future['yhat'].sum()
                st.metric("30-Day Total", format_currency(total_30d))
            
            with col3:
                trend_change = ((forecast_future['yhat'].iloc[-1] - forecast_future['yhat'].iloc[0]) / forecast_future['yhat'].iloc[0] * 100)
                st.metric("Expected Trend", f"{trend_change:+.1f}%")
            
            # Decomposition
            st.markdown("**Forecast Components**")
            fig = model.plot_components(forecast, include_legend=True)
            st.pyplot(fig, use_container_width=True)
    else:
        st.warning("⚠️ Insufficient data for forecasting. Need at least 21 days of historical data.")

# ============================================================================
# PAGE 6: REPORTS & EXPORT
# ============================================================================

elif page == "Reports":
    st.markdown(f"<div class='header-title'>Reports & Export</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Download dashboards and analytics</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Executive Summary", "Detailed Report", "Data Export"])
    
    with tab1:
        st.markdown("**Executive Summary Report**")
        
        report_data = generate_report_data(filtered_df)
        
        summary_text = f"""
        # RAYMOND RETAIL INTELLIGENCE - EXECUTIVE SUMMARY
        
        ## Key Metrics
        - Total Sales: {format_currency(report_data['total_sales'])}
        - Total Profit: {format_currency(report_data['total_profit'])}
        - Average Order Value: {format_currency(report_data['avg_order_value'])}
        - Store Footfall: {format_number(report_data['total_footfall'])}
        - Inventory Turnover: {report_data['inventory_turnover']:.2f}x
        
        ## Top Performers
        - Top Store: {report_data['top_store']} (${report_data['top_store_sales']:,.0f})
        - Top Category: {report_data['top_category']} (${report_data['top_category_sales']:,.0f})
        - Average Profit Margin: {report_data['avg_profit_margin']:.1f}%
        
        ## Insights
        {report_data['insights']}
        
        Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        st.markdown(summary_text)
        
        # Download as text
        st.download_button(
            label="📄 Download Executive Summary (TXT)",
            data=summary_text,
            file_name=f"Raymond_Executive_Summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with tab2:
        st.markdown("**Detailed Analytics Report**")
        
        # Generate detailed data
        report_df = filtered_df.groupby(['date', 'store_name', 'category']).agg({
            'sales': 'sum',
            'profit': 'sum',
            'quantity': 'sum',
            'footfall': 'sum',
            'stock': 'mean',
            'price': 'mean'
        }).reset_index()
        
        report_df['profit_margin'] = (report_df['profit'] / report_df['sales'] * 100).round(2)
        
        st.dataframe(report_df.sort_values('date', ascending=False), use_container_width=True)
        
        # Download as CSV
        csv = report_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Detailed Report (CSV)",
            data=csv,
            file_name=f"Raymond_Detailed_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.markdown("**Raw Data Export**")
        
        export_options = st.multiselect(
            "Select datasets to export",
            ["Sales Data", "Customer Data", "Inventory Data"],
            default=["Sales Data"]
        )
        
        if st.button("🔄 Generate Export"):
            if "Sales Data" in export_options:
                st.info("📦 Sales Data (Last 100 rows)")
                st.dataframe(filtered_df.sort_values('date', ascending=False).head(100), use_container_width=True)
                
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Sales Data (CSV)",
                    data=csv,
                    file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="sales_export"
                )
            
            if "Customer Data" in export_options:
                st.info("👥 Customer Data (Sample)")
                st.dataframe(customer_df.head(100), use_container_width=True)
                
                csv = customer_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Customer Data (CSV)",
                    data=csv,
                    file_name=f"customer_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="customer_export"
                )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 0.85rem; margin-top: 2rem;'>
    <p>Raymond Retail Intelligence Dashboard • Powered by Streamlit & Prophet • Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True)
