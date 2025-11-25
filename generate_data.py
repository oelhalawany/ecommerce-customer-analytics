"""
Generate Realistic E-Commerce Data
This script creates synthetic customer and transaction data for analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("🚀 Generating E-Commerce Data...")

# Configuration
N_CUSTOMERS = 5000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 11, 25)
PRODUCTS = [
    {'name': 'Laptop', 'price': 899, 'category': 'Electronics'},
    {'name': 'Smartphone', 'price': 599, 'category': 'Electronics'},
    {'name': 'Headphones', 'price': 89, 'category': 'Electronics'},
    {'name': 'T-Shirt', 'price': 25, 'category': 'Clothing'},
    {'name': 'Jeans', 'price': 59, 'category': 'Clothing'},
    {'name': 'Sneakers', 'price': 79, 'category': 'Footwear'},
    {'name': 'Backpack', 'price': 49, 'category': 'Accessories'},
    {'name': 'Watch', 'price': 199, 'category': 'Accessories'},
    {'name': 'Book', 'price': 15, 'category': 'Books'},
    {'name': 'Coffee Maker', 'price': 79, 'category': 'Home'},
]

# 1. Generate Customers
print("📊 Creating customers...")

customers = pd.DataFrame({
    'customer_id': range(1, N_CUSTOMERS + 1),
    'age': np.random.randint(18, 70, N_CUSTOMERS),
    'gender': np.random.choice(['Male', 'Female', 'Other'], N_CUSTOMERS, p=[0.48, 0.48, 0.04]),
    'country': np.random.choice(['Germany', 'Austria', 'Switzerland', 'Netherlands', 'Belgium'], 
                                N_CUSTOMERS, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
    'signup_date': [START_DATE + timedelta(days=random.randint(0, 730)) for _ in range(N_CUSTOMERS)],
    'marketing_channel': np.random.choice(['Social Media', 'Google Ads', 'Email', 'Organic', 'Referral'], 
                                          N_CUSTOMERS, p=[0.3, 0.25, 0.2, 0.15, 0.1])
})

customers.to_csv('data/customers.csv', index=False)
print(f"✅ Created {len(customers)} customers")

# 2. Generate Transactions
print("💳 Creating transactions...")

transactions = []
transaction_id = 1

for customer_id in range(1, N_CUSTOMERS + 1):
    signup_date = customers.loc[customers['customer_id'] == customer_id, 'signup_date'].values[0]
    
    # Determine customer behavior type
    customer_type = np.random.choice(['loyal', 'occasional', 'one-time', 'churned'], 
                                     p=[0.2, 0.4, 0.25, 0.15])
    
    if customer_type == 'loyal':
        n_transactions = np.random.randint(10, 50)
    elif customer_type == 'occasional':
        n_transactions = np.random.randint(3, 10)
    elif customer_type == 'one-time':
        n_transactions = 1
    else:  # churned
        n_transactions = np.random.randint(2, 8)
    
    for i in range(n_transactions):
        # Generate transaction date
        if customer_type == 'churned':
            # Churned customers stopped buying 6+ months ago
            max_days = (END_DATE - pd.Timestamp(signup_date)).days - 180
        else:
            max_days = (END_DATE - pd.Timestamp(signup_date)).days
        
        if max_days <= 0:
            continue
            
        days_after_signup = random.randint(0, max_days)
        transaction_date = pd.Timestamp(signup_date) + timedelta(days=days_after_signup)
        
        # Select random product
        product = random.choice(PRODUCTS)
        quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
        
        # Add some price variation
        price = product['price'] * (1 + np.random.uniform(-0.1, 0.1))
        total_amount = price * quantity
        
        transactions.append({
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'transaction_date': transaction_date,
            'product_name': product['name'],
            'product_category': product['category'],
            'quantity': quantity,
            'unit_price': round(price, 2),
            'total_amount': round(total_amount, 2)
        })
        
        transaction_id += 1

transactions_df = pd.DataFrame(transactions)
transactions_df = transactions_df.sort_values('transaction_date').reset_index(drop=True)
transactions_df.to_csv('data/transactions.csv', index=False)
print(f"✅ Created {len(transactions_df)} transactions")

# 3. Generate Summary Statistics
print("\n📈 Data Summary:")
print(f"   Total Customers: {len(customers):,}")
print(f"   Total Transactions: {len(transactions_df):,}")
print(f"   Date Range: {transactions_df['transaction_date'].min().date()} to {transactions_df['transaction_date'].max().date()}")
print(f"   Total Revenue: €{transactions_df['total_amount'].sum():,.2f}")
print(f"   Average Order Value: €{transactions_df['total_amount'].mean():.2f}")
print(f"   Average Transactions per Customer: {len(transactions_df) / len(customers):.1f}")

print("\n✨ Data generation complete!")
print("📁 Files saved:")
print("   - data/customers.csv")
print("   - data/transactions.csv")
print("\n🎯 Next step: Open notebooks/01_explore_data.ipynb")
