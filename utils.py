import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================================
# COLOR PALETTE - LUXURY/REFINED AESTHETIC
# ============================================================================

color_palette = {
    'primary': '#0F1419',      # Very dark navy
    'secondary': '#1E88E5',    # Professional blue
    'accent': '#FFD700',       # Gold
    'success': '#10B981',      # Emerald green
    'warning': '#FFC107',      # Amber
    'danger': '#DC3545',       # Red
    'dark': '#0F1419',         # Dark background
    'light': '#E8E8E8'         # Light text
}

# ============================================================================
# FORMATTING FUNCTIONS
# ============================================================================

def format_currency(value, decimals=0):
    """Format value as currency"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.{decimals}f}M"
    elif value >= 1_000:
        return f"${value/1_000:.{decimals}f}K"
    else:
        return f"${value:,.{decimals}f}"


def format_number(value):
    """Format number with thousands separator"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:,.0f}"


def format_percentage(value, decimals=1):
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"


# ============================================================================
# KPI CALCULATION FUNCTIONS
# ============================================================================

def calculate_kpis(filtered_df, full_df):
    """
    Calculate comprehensive KPIs for the dashboard
    """
    
    # Current period metrics
    total_sales = filtered_df['sales'].sum()
    total_profit = filtered_df['profit'].sum()
    total_footfall = filtered_df['footfall'].sum()
    
    # AOV (Average Order Value)
    total_orders = len(filtered_df)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    # Inventory turnover
    avg_stock = filtered_df['stock'].mean()
    total_quantity = filtered_df['quantity'].sum()
    inventory_turnover = total_quantity / avg_stock if avg_stock > 0 else 0
    
    # Previous period (last 30 days before current period)
    filtered_dates = pd.to_datetime(filtered_df['date'])
    if len(filtered_dates) > 0:
        min_date = filtered_dates.min()
        period_days = (filtered_dates.max() - min_date).days + 1
        
        previous_period_start = min_date - timedelta(days=period_days)
        previous_period_end = min_date - timedelta(days=1)
        
        prev_df = full_df[
            (pd.to_datetime(full_df['date']) >= previous_period_start) &
            (pd.to_datetime(full_df['date']) <= previous_period_end)
        ]
    else:
        prev_df = pd.DataFrame()
    
    # Calculate changes
    if len(prev_df) > 0:
        prev_sales = prev_df['sales'].sum()
        prev_profit = prev_df['profit'].sum()
        prev_footfall = prev_df['footfall'].sum()
        prev_aov = prev_sales / len(prev_df) if len(prev_df) > 0 else 0
        
        sales_change = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
        profit_change = ((total_profit - prev_profit) / prev_profit * 100) if prev_profit > 0 else 0
        footfall_change = ((total_footfall - prev_footfall) / prev_footfall * 100) if prev_footfall > 0 else 0
        aov_change = ((avg_order_value - prev_aov) / prev_aov * 100) if prev_aov > 0 else 0
    else:
        sales_change = 0
        profit_change = 0
        footfall_change = 0
        aov_change = 0
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'avg_order_value': avg_order_value,
        'total_footfall': int(total_footfall),
        'inventory_turnover': inventory_turnover,
        'sales_change': sales_change,
        'profit_change': profit_change,
        'footfall_change': footfall_change,
        'aov_change': aov_change,
        'total_orders': total_orders
    }


# ============================================================================
# AI INSIGHTS GENERATION
# ============================================================================

def get_ai_insights(df, kpis):
    """
    Generate AI-driven business insights based on data
    """
    insights = []
    
    # Sales trend insight
    if len(df) > 1:
        recent_sales = df.nlargest(7, 'date')['sales'].mean()
        older_sales = df.nsmallest(7, 'date')['sales'].mean()
        
        if recent_sales > older_sales * 1.1:
            insights.append("📈 Strong upward momentum detected. Sales trending up by " + 
                          f"{((recent_sales - older_sales) / older_sales * 100):.1f}% vs. earlier period.")
        elif recent_sales < older_sales * 0.9:
            insights.append("📉 Sales showing downward pressure. Consider promotional campaigns or inventory review.")
    
    # Category performance
    top_category = df.groupby('category')['sales'].sum().nlargest(1)
    if len(top_category) > 0:
        cat_name = top_category.index[0]
        cat_pct = (top_category.values[0] / df['sales'].sum() * 100)
        insights.append(f"🏆 {cat_name} is your top performer, contributing {cat_pct:.1f}% of total sales.")
    
    # Profit margin analysis
    avg_margin = (df['profit'].sum() / df['sales'].sum() * 100) if df['sales'].sum() > 0 else 0
    if avg_margin < 25:
        insights.append(f"⚠️ Average profit margin is low at {avg_margin:.1f}%. Review pricing strategy and cost management.")
    elif avg_margin > 45:
        insights.append(f"💰 Excellent profit margin of {avg_margin:.1f}%. Maintain current pricing and quality standards.")
    
    # Footfall conversion
    conversion_rate = (df['sales'].sum() / df['footfall'].sum() * 100) if df['footfall'].sum() > 0 else 0
    if conversion_rate > 0:
        insights.append(f"🎯 Store conversion rate is {conversion_rate:.1f}%. Focus on improving customer experience to boost this metric.")
    
    # Stock health
    avg_stock = df['stock'].mean()
    total_quantity = df['quantity'].sum()
    turnover = total_quantity / avg_stock if avg_stock > 0 else 0
    
    if turnover < 1.5:
        insights.append("📦 Inventory turnover is slow. Consider promotions or inventory optimization.")
    elif turnover > 3:
        insights.append("⚡ High inventory turnover indicates strong demand. Consider increasing stock levels.")
    
    # Promotion effectiveness
    promo_df = df[df['promotion_type'] != 'None']
    if len(promo_df) > 0:
        promo_margin = (promo_df['profit'].sum() / promo_df['sales'].sum() * 100)
        no_promo_df = df[df['promotion_type'] == 'None']
        if len(no_promo_df) > 0:
            no_promo_margin = (no_promo_df['profit'].sum() / no_promo_df['sales'].sum() * 100)
            if promo_margin < no_promo_margin * 0.8:
                insights.append("🎁 Promotions may be eroding margins. Review discount structure and thresholds.")
    
    return insights


# ============================================================================
# ALERT GENERATION
# ============================================================================

def create_alert_list(df):
    """
    Generate inventory and business alerts
    """
    alerts = []
    
    # Low stock alert
    low_stock = df[df['stock'] < 10]
    if len(low_stock) > 0:
        alerts.append(
            ("low_stock", 
             f"{len(low_stock)} items have critically low stock levels (<10 units). Immediate reorder recommended.",
             "critical")
        )
    
    # Slow moving inventory
    slow_moving = df[df['quantity'] < 1]  # Items not selling
    if len(slow_moving) > 3:
        alerts.append(
            ("slow_moving",
             f"{len(slow_moving)} products have minimal sales. Consider markdowns or discontinuation.",
             "warning")
        )
    
    # High inventory ratio
    high_inventory = df[df['stock'] > df['quantity'].mean() * 10]
    if len(high_inventory) > 0 and len(df) > 0:
        pct = (len(high_inventory) / len(df) * 100)
        if pct > 15:
            alerts.append(
                ("overstocking",
                 f"{pct:.0f}% of items are overstocked. Review demand forecasting and reduce procurement.",
                 "warning")
            )
    
    # Sales decline
    if len(df) > 2:
        recent_avg = df.nlargest(5, 'date')['sales'].mean()
        older_avg = df.nsmallest(5, 'date')['sales'].mean()
        if recent_avg < older_avg * 0.7:
            alerts.append(
                ("sales_decline",
                 f"Sales have declined by {((1 - recent_avg/older_avg) * 100):.1f}% recently. Investigate root causes.",
                 "critical")
            )
    
    # Zero margin products
    zero_margin = df[df['profit'] <= 0]
    if len(zero_margin) > 0:
        alerts.append(
            ("negative_margin",
             f"{len(zero_margin)} transactions have zero or negative margins. Review pricing immediately.",
             "critical")
        )
    
    return alerts


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_report_data(df):
    """
    Generate data for comprehensive reports
    """
    
    total_sales = df['sales'].sum()
    total_profit = df['profit'].sum()
    avg_order_value = total_sales / len(df) if len(df) > 0 else 0
    total_footfall = df['footfall'].sum()
    
    # Top performers
    top_store = df.groupby('store_name')['sales'].sum().idxmax() if len(df) > 0 else "N/A"
    top_store_sales = df.groupby('store_name')['sales'].sum().max() if len(df) > 0 else 0
    
    top_category = df.groupby('category')['sales'].sum().idxmax() if len(df) > 0 else "N/A"
    top_category_sales = df.groupby('category')['sales'].sum().max() if len(df) > 0 else 0
    
    avg_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    # Generate insights text
    insights_list = get_ai_insights(df, {})
    insights_text = "\n".join([f"- {insight}" for insight in insights_list[:3]])
    
    inventory_turnover = df['quantity'].sum() / df['stock'].mean() if df['stock'].mean() > 0 else 0
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'avg_order_value': avg_order_value,
        'total_footfall': int(total_footfall),
        'top_store': top_store,
        'top_store_sales': top_store_sales,
        'top_category': top_category,
        'top_category_sales': top_category_sales,
        'avg_profit_margin': avg_profit_margin,
        'insights': insights_text,
        'inventory_turnover': inventory_turnover
    }


# ============================================================================
# SEGMENTATION UTILITIES
# ============================================================================

def segment_customers(customer_df, num_segments=4):
    """
    Segment customers based on RFM analysis
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    # Prepare features
    features = customer_df[['total_spend', 'num_purchases', 'avg_order_value']].copy()
    
    # Standardize
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Clustering
    kmeans = KMeans(n_clusters=num_segments, random_state=42, n_init=10)
    segments = kmeans.fit_predict(features_scaled)
    
    return segments


# ============================================================================
# STATISTICAL UTILITIES
# ============================================================================

def calculate_confidence_interval(data, confidence=0.95):
    """
    Calculate confidence interval for data
    """
    from scipy import stats
    
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    ci = std_err * stats.t.ppf((1 + confidence) / 2.0, n - 1)
    
    return mean - ci, mean + ci


def detect_outliers(data, method='iqr'):
    """
    Detect outliers using IQR or Z-score method
    """
    if method == 'iqr':
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (data < lower_bound) | (data > upper_bound)
    else:  # z-score
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        outliers = z_scores > 3
    
    return outliers
