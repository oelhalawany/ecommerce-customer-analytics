"""
Common utility functions for data analysis

Usage in notebooks:
    import sys
    sys.path.append('../')
    from src.common import load_data, calculate_rfm
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_data(customers_path='../data/customers.csv', 
              transactions_path='../data/transactions.csv'):
    """
    Load customer and transaction data
    
    Returns:
        tuple: (customers_df, transactions_df)
    """
    customers = pd.read_csv(customers_path)
    transactions = pd.read_csv(transactions_path)
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    
    print(f"✅ Loaded {len(customers):,} customers")
    print(f"✅ Loaded {len(transactions):,} transactions")
    
    return customers, transactions


def calculate_rfm(transactions, analysis_date=None):
    """
    Calculate RFM (Recency, Frequency, Monetary) scores
    
    Args:
        transactions: DataFrame with transaction data
        analysis_date: Reference date for recency (default: max transaction date)
    
    Returns:
        DataFrame: RFM scores for each customer
    """
    if analysis_date is None:
        analysis_date = transactions['transaction_date'].max()
    
    rfm = transactions.groupby('customer_id').agg({
        'transaction_date': lambda x: (analysis_date - x.max()).days,
        'transaction_id': 'count',
        'total_amount': 'sum'
    }).reset_index()
    
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    return rfm


def segment_customer(recency, frequency, monetary):
    """
    Assign customer segment based on RFM values
    
    Args:
        recency: Days since last purchase
        frequency: Number of purchases
        monetary: Total spend
    
    Returns:
        str: Customer segment name
    """
    if recency > 180:
        return 'Churned'
    elif frequency >= 10 and monetary >= 1000:
        return 'Champion'
    elif frequency >= 5:
        return 'Loyal'
    elif frequency >= 2:
        return 'Occasional'
    else:
        return 'One-time'


def get_segment_summary(rfm_df):
    """
    Get summary statistics by customer segment
    
    Args:
        rfm_df: DataFrame with RFM scores and segments
    
    Returns:
        DataFrame: Summary by segment
    """
    summary = rfm_df.groupby('segment').agg({
        'customer_id': 'count',
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': ['mean', 'sum']
    }).round(2)
    
    summary.columns = ['count', 'avg_recency', 'avg_frequency', 'avg_monetary', 'total_revenue']
    
    return summary.sort_values('total_revenue', ascending=False)


# Add your own functions below:
# def my_custom_function():
#     pass
