#!/usr/bin/env python3
"""
KPI Analysis and Visualization Script
Reads parquet files from migrate/data directory and creates comprehensive visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Configuration
DATA_DIR = "./.claude/skills/migrate/data/2026-09-06_00-33-01/"
OUTPUT_DIR = "./.claude/skills/visualize/figures/"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def load_data():
    """Load parquet files"""
    print("Loading data...")
    fact_sales = pd.read_parquet(os.path.join(DATA_DIR, "fact_sales.parquet"))
    dim_customer = pd.read_parquet(os.path.join(DATA_DIR, "dim_customer.parquet"))
    return fact_sales, dim_customer


def create_dimension_tables(fact_sales):
    """Create synthetic dimension tables for date, store, and product"""
    print("Creating dimension tables...")

    # Create date dimension
    min_date_sk = fact_sales['date_sk'].min()
    max_date_sk = fact_sales['date_sk'].max()
    base_date = datetime(2024, 1, 1)

    dates = []
    for sk in range(int(min_date_sk), int(max_date_sk) + 1):
        current_date = base_date + timedelta(days=sk - 1)
        dates.append({
            'date_sk': sk,
            'date': current_date,
            'year': current_date.year,
            'month': current_date.month,
            'day': current_date.day,
            'quarter': (current_date.month - 1) // 3 + 1,
            'week': current_date.isocalendar()[1],
            'day_name': current_date.strftime('%A')
        })
    dim_date = pd.DataFrame(dates)

    # Create store dimension
    store_sks = fact_sales['store_sk'].unique()
    dim_store = pd.DataFrame({
        'store_sk': store_sks,
        'store_name': [f'Store {int(sk)}' for sk in store_sks],
        'store_code': [f'STR-{int(sk):05d}' for sk in store_sks],
        'region': np.random.choice(['North', 'South', 'East', 'West'], len(store_sks))
    })

    # Create product dimension
    product_sks = fact_sales['product_sk'].unique()
    categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Food']
    dim_product = pd.DataFrame({
        'product_sk': product_sks,
        'product_name': [f'Product {int(sk)}' for sk in product_sks],
        'product_code': [f'PRD-{int(sk):05d}' for sk in product_sks],
        'category': np.random.choice(categories, len(product_sks))
    })

    return dim_date, dim_store, dim_product


def calculate_kpis(fact_sales, dim_customer):
    """Calculate KPIs"""
    print("Calculating KPIs...")

    kpis = {}

    # Total Sales (gross amount)
    kpis['Total_Sales'] = fact_sales['gross_amount'].sum()

    # Total Returns (based on negative amounts - if applicable)
    # Since we don't have explicit returns, we'll calculate it differently
    kpis['Total_Returns'] = 0  # No explicit returns in data

    # Net Sales
    kpis['Net_Sales'] = fact_sales['net_amount'].sum()

    # Average Sales per Store
    kpis['Avg_Sales_per_Store'] = fact_sales.groupby('store_sk')['net_amount'].sum().mean()

    # Average Sales per Product
    kpis['Avg_Sales_per_Product'] = fact_sales.groupby('product_sk')['net_amount'].sum().mean()

    # Average Sales per Customer
    kpis['Avg_Sales_per_Customer'] = fact_sales.groupby('customer_sk')['net_amount'].sum().mean()

    return kpis


def create_visualizations(fact_sales, dim_date, dim_store, dim_product, dim_customer):
    """Create all visualizations"""

    # Merge data for enriched analysis
    sales_enriched = fact_sales.merge(dim_date, on='date_sk', how='left')
    sales_enriched = sales_enriched.merge(dim_store, on='store_sk', how='left')
    sales_enriched = sales_enriched.merge(dim_product, on='product_sk', how='left')
    sales_enriched = sales_enriched.merge(dim_customer, on='customer_sk', how='left')

    # 1. Sales Trend over Time
    print("Creating Sales Trend over Time...")
    daily_sales = sales_enriched.groupby('date')['net_amount'].sum().reset_index()
    daily_sales = daily_sales.sort_values('date')

    plt.figure(figsize=(14, 6))
    plt.plot(daily_sales['date'], daily_sales['net_amount'], linewidth=2, color='#2E86AB')
    plt.fill_between(daily_sales['date'], daily_sales['net_amount'], alpha=0.3, color='#2E86AB')
    plt.title('Sales Trend over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Net Sales Amount ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '01_sales_trend_over_time.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Sales by Store
    print("Creating Sales by Store...")
    store_sales = sales_enriched.groupby('store_name')['net_amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    store_sales.plot(kind='bar', color='#A23B72')
    plt.title('Sales by Store', fontsize=16, fontweight='bold')
    plt.xlabel('Store', fontsize=12)
    plt.ylabel('Net Sales Amount ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '02_sales_by_store.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Sales by Product
    print("Creating Sales by Product...")
    product_sales = sales_enriched.groupby('category')['net_amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(product_sales)))
    product_sales.plot(kind='bar', color=colors)
    plt.title('Sales by Product Category', fontsize=16, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Net Sales Amount ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '03_sales_by_product.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Sales by Customer
    print("Creating Sales by Customer...")
    top_customers = sales_enriched.groupby('customer_code')['net_amount'].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    top_customers.plot(kind='barh', color='#F18F01')
    plt.title('Top 10 Customers by Sales', fontsize=16, fontweight='bold')
    plt.xlabel('Net Sales Amount ($)', fontsize=12)
    plt.ylabel('Customer', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '04_sales_by_customer.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Returns Trend Over Time (Discount Amount as proxy)
    print("Creating Returns/Discounts Trend Over Time...")
    daily_discounts = sales_enriched.groupby('date')['discount_amount'].sum().reset_index()
    daily_discounts = daily_discounts.sort_values('date')

    plt.figure(figsize=(14, 6))
    plt.plot(daily_discounts['date'], daily_discounts['discount_amount'], linewidth=2, color='#C1121F')
    plt.fill_between(daily_discounts['date'], daily_discounts['discount_amount'], alpha=0.3, color='#C1121F')
    plt.title('Discounts Trend over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Discount Amount ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '05_discounts_trend_over_time.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Returns by Store (Discounts by Store)
    print("Creating Discounts by Store...")
    store_discounts = sales_enriched.groupby('store_name')['discount_amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    store_discounts.plot(kind='bar', color='#C1121F')
    plt.title('Discounts by Store', fontsize=16, fontweight='bold')
    plt.xlabel('Store', fontsize=12)
    plt.ylabel('Discount Amount ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '06_discounts_by_store.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 7. Returns by Product (Discounts by Category)
    print("Creating Discounts by Product...")
    product_discounts = sales_enriched.groupby('category')['discount_amount'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(product_discounts)))
    product_discounts.plot(kind='bar', color=colors)
    plt.title('Discounts by Product Category', fontsize=16, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Discount Amount ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '07_discounts_by_product.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 8. Returns by Customer (Discounts by Customer)
    print("Creating Discounts by Customer...")
    top_customer_discounts = sales_enriched.groupby('customer_code')['discount_amount'].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    top_customer_discounts.plot(kind='barh', color='#C1121F')
    plt.title('Top 10 Customers by Discounts Received', fontsize=16, fontweight='bold')
    plt.xlabel('Discount Amount ($)', fontsize=12)
    plt.ylabel('Customer', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '08_discounts_by_customer.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print("All visualizations created successfully!")


def print_kpis(kpis):
    """Print KPIs in a formatted table"""
    print("\n" + "=" * 60)
    print("KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 60)
    print(f"Total Sales:                 ${kpis['Total_Sales']:,.2f}")
    print(f"Total Returns:               ${kpis['Total_Returns']:,.2f}")
    print(f"Net Sales:                   ${kpis['Net_Sales']:,.2f}")
    print(f"Average Sales per Store:     ${kpis['Avg_Sales_per_Store']:,.2f}")
    print(f"Average Sales per Product:   ${kpis['Avg_Sales_per_Product']:,.2f}")
    print(f"Average Sales per Customer:  ${kpis['Avg_Sales_per_Customer']:,.2f}")
    print("=" * 60 + "\n")


def main():
    """Main execution function"""
    print(f"\n{'=' * 60}")
    print("KPI ANALYSIS AND VISUALIZATION")
    print(f"{'=' * 60}\n")

    # Load data
    fact_sales, dim_customer = load_data()

    # Create dimension tables
    dim_date, dim_store, dim_product = create_dimension_tables(fact_sales)

    # Calculate KPIs
    kpis = calculate_kpis(fact_sales, dim_customer)
    print_kpis(kpis)

    # Create visualizations
    create_visualizations(fact_sales, dim_date, dim_store, dim_product, dim_customer)

    print(f"Visualizations saved to: {OUTPUT_DIR}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
