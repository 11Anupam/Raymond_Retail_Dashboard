import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(days=365, num_stores=15, num_transactions=5000):
    """
    Generate realistic synthetic retail data for fashion brand
    """
    np.random.seed(42)
    
    stores = [f"Store {chr(65+i)}" for i in range(num_stores)]
    categories = ["Menswear", "Womenswear", "Accessories", "Footwear", "Activewear"]
    promotion_types = ["None", "Discount", "BOGO", "Seasonal Sale", "Clearance"]
    
    # Date range
    start_date = datetime.now() - timedelta(days=days)
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    
    data = []
    
    for _ in range(num_transactions):
        date = np.random.choice(dates)
        store = np.random.choice(stores)
        category = np.random.choice(categories)
        
        # Price varies by category
        base_price = {
            "Menswear": np.random.uniform(50, 200),
            "Womenswear": np.random.uniform(60, 250),
            "Accessories": np.random.uniform(20, 100),
            "Footwear": np.random.uniform(80, 250),
            "Activewear": np.random.uniform(40, 150)
        }[category]
        
        quantity = np.random.randint(1, 8)
        price = base_price * np.random.uniform(0.8, 1.2)
        sales = quantity * price
        
        # Profit margin 30-50%
        profit_margin = np.random.uniform(0.30, 0.50)
        profit = sales * profit_margin
        
        # Stock levels
        stock = np.random.randint(5, 200)
        
        # Footfall (customers who entered, not all bought)
        footfall = np.random.randint(10, 100)
        
        # Promotion
        promotion = np.random.choice(promotion_types, p=[0.5, 0.2, 0.15, 0.1, 0.05])
        
        # Seasonal adjustment (higher sales in certain months)
        month = date.month
        seasonal_factor = {
            1: 0.8, 2: 0.9, 3: 1.0, 4: 1.1, 5: 1.0,
            6: 0.9, 7: 1.2, 8: 1.3, 9: 1.1, 10: 0.95,
            11: 1.4, 12: 1.5  # Peak season
        }.get(month, 1.0)
        
        sales *= seasonal_factor
        profit *= seasonal_factor
        
        data.append({
            'date': date,
            'store_name': store,
            'category': category,
            'sales': sales,
            'profit': profit,
            'quantity': quantity,
            'price': price,
            'stock': stock,
            'footfall': footfall,
            'promotion_type': promotion,
            'cost': sales * (1 - profit_margin)
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    return df


def generate_customer_data(num_customers=1000):
    """
    Generate customer transaction history and behavior data
    """
    np.random.seed(42)
    
    data = []
    
    for i in range(num_customers):
        # Customer segment
        segment = np.random.choice(
            ['Premium', 'Regular', 'New', 'At-Risk'],
            p=[0.15, 0.50, 0.20, 0.15]
        )
        
        # Purchase behavior by segment
        if segment == 'Premium':
            num_purchases = np.random.randint(20, 100)
            avg_order_value = np.random.uniform(150, 400)
            total_spend = num_purchases * avg_order_value
        elif segment == 'Regular':
            num_purchases = np.random.randint(5, 25)
            avg_order_value = np.random.uniform(80, 200)
            total_spend = num_purchases * avg_order_value
        elif segment == 'New':
            num_purchases = np.random.randint(1, 5)
            avg_order_value = np.random.uniform(50, 150)
            total_spend = num_purchases * avg_order_value
        else:  # At-Risk
            num_purchases = np.random.randint(3, 15)
            avg_order_value = np.random.uniform(60, 180)
            total_spend = num_purchases * avg_order_value
        
        # Days since last purchase
        if segment == 'At-Risk':
            days_since = np.random.randint(60, 365)
        else:
            days_since = np.random.randint(0, 90)
        
        # Additional metrics
        return_rate = np.random.uniform(0, 0.2) if segment != 'Premium' else np.random.uniform(0, 0.05)
        
        data.append({
            'customer_id': f'C{i:06d}',
            'segment': segment,
            'total_spend': total_spend,
            'num_purchases': num_purchases,
            'avg_order_value': avg_order_value,
            'days_since_purchase': days_since,
            'return_rate': return_rate,
            'lifetime_value': total_spend * (1 - return_rate),
            'preferred_category': np.random.choice(['Menswear', 'Womenswear', 'Accessories', 'Footwear', 'Activewear']),
            'signup_date': (datetime.now() - timedelta(days=np.random.randint(30, 730))).date()
        })
    
    return pd.DataFrame(data)
