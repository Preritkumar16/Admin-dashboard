import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_admin_data():
    """Generate sample admin dashboard data"""
    
    # Create data directory if it doesn't exist
    os.makedirs('python-dashboard/data', exist_ok=True)
    
    np.random.seed(42)
    
    n_orders = 500
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food']
    statuses = ['delivered', 'pending', 'processing', 'cancelled']
    
    # Generate dates
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=np.random.randint(0, 90)) for _ in range(n_orders)]
    
    # Generate data
    data = {
        'order_id': [f'ORD{str(i).zfill(6)}' for i in range(1, n_orders + 1)],
        'timestamp': dates,
        'customer_id': np.random.randint(1, 101, n_orders),
        'amount': np.random.randint(100, 10000, n_orders),
        'category': np.random.choice(categories, n_orders),
        'status': np.random.choice(statuses, n_orders, p=[0.5, 0.2, 0.2, 0.1])
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp')
    
    # Save to CSV
    df.to_csv('python-dashboard/data/dashboard_data.csv', index=False)
    print(f"Generated {n_orders} orders data")
    return df

if __name__ == '__main__':
    generate_admin_data()
