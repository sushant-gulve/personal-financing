import pandas as pd
import os
import re
from datetime import datetime

def categorize_transactions(df):
    """
    Categorize transactions based on narration patterns
    """
    
    # Define categorization rules
    categories = {
        'Food & Dining': [
            'ZOMATO', 'SWIGGY', 'ARUMUGAM', 'RESTAURANT', 'FOOD', 'CAFE', 'HOTEL',
            'DHABA', 'MESS', 'CANTEEN', 'LUNCH', 'DINNER', 'BREAKFAST'
        ],
        'Shopping & Retail': [
            'DECATHLON', 'PARKAR SHIRTS', 'CLOTH STORES', 'TRADING CO', 'COLLECTION',
            'SPORTS', 'AMAZON', 'FLIPKART', 'MYNTRA', 'AJIO', 'RETAIL', 'MART',
            'STORE', 'SHOPPING', 'MALL'
        ],
        'Transportation': [
            'UBER', 'OLA', 'RAPIDO', 'TAXI', 'AUTO', 'BUS', 'TRAIN', 'METRO',
            'PETROL', 'FUEL', 'DIESEL', 'TRANSPORT', 'TRAVEL', 'BOOKING'
        ],
        'Entertainment & Subscriptions': [
            'SPOTIFY', 'NETFLIX', 'AMAZON PRIME', 'YOUTUBE', 'ENTERTAINMENT',
            'MOVIE', 'CINEMA', 'GAMES', 'SUBSCRIPTION', 'MUSIC', 'UDEMY',
            'LINKEDIN', 'COURSERA'
        ],
        'Utilities & Bills': [
            'ELECTRICITY', 'WATER', 'GAS', 'INTERNET', 'MOBILE', 'PHONE',
            'BROADBAND', 'WIFI', 'BILL', 'RECHARGE', 'PAYMENT', 'UTILITY'
        ],
        'Banking & Finance': [
            'BANK', 'ATM', 'INTEREST', 'CHARGES', 'FEE', 'PENALTY', 'LOAN',
            'EMI', 'INSURANCE', 'PREMIUM', 'INVESTMENT', 'MUTUAL FUND',
            'DIVIDEND', 'TATA MOTORS', 'ZERODHA', 'TRADING', 'DEMAT'
        ],
        'Healthcare': [
            'HOSPITAL', 'CLINIC', 'DOCTOR', 'MEDICAL', 'PHARMACY', 'MEDICINE',
            'HEALTH', 'DIAGNOSTIC', 'LAB', 'CHECKUP'
        ],
        'Education': [
            'SCHOOL', 'COLLEGE', 'UNIVERSITY', 'EDUCATION', 'COURSE', 'TRAINING',
            'FEES', 'TUITION', 'BOOKS', 'STATIONERY'
        ],
        'Technology & Software': [
            'GOOGLE', 'MICROSOFT', 'APPLE', 'SOFTWARE', 'CLOUD', 'HOSTING',
            'DOMAIN', 'TECH', 'COMPUTER', 'MOBILE', 'GADGET'
        ],
        'Cash & ATM': [
            'ATW', 'ATM', 'CASH', 'WITHDRAWAL'
        ],
        'Income & Salary': [
            'SALARY', 'NEFT CR', 'IMPS CR', 'ACH C', 'CREDIT', 'INCOME',
            'BONUS', 'INCENTIVE', 'REFUND', 'CASHBACK'
        ],
        'Investments & Savings': [
            'INVESTMENT', 'MUTUAL FUND', 'SIP', 'FIXED DEPOSIT', 'RD',
            'RECURRING DEPOSIT', 'SAVINGS', 'PORTFOLIO'
        ]
    }
    
    # Create a copy for categorization
    df_categorized = df.copy()
    df_categorized['Category'] = 'Others'
    df_categorized['Subcategory'] = 'Miscellaneous'
    
    # Apply categorization rules
    for category, keywords in categories.items():
        for keyword in keywords:
            mask = df_categorized['Narration'].str.contains(keyword, case=False, na=False)
            df_categorized.loc[mask, 'Category'] = category
            
            # Set subcategory based on specific patterns
            if category == 'Food & Dining':
                if any(word in keyword.lower() for word in ['zomato', 'swiggy']):
                    df_categorized.loc[mask, 'Subcategory'] = 'Online Food Delivery'
                else:
                    df_categorized.loc[mask, 'Subcategory'] = 'Restaurant/Local Food'
            elif category == 'Banking & Finance':
                if 'INTEREST' in keyword:
                    df_categorized.loc[mask, 'Subcategory'] = 'Bank Interest'
                elif 'DIVIDEND' in keyword or 'TATA MOTORS' in keyword:
                    df_categorized.loc[mask, 'Subcategory'] = 'Dividend Income'
                elif 'ZERODHA' in keyword:
                    df_categorized.loc[mask, 'Subcategory'] = 'Trading/Investment'
                else:
                    df_categorized.loc[mask, 'Subcategory'] = 'Banking Services'
            elif category == 'Income & Salary':
                if any(word in keyword for word in ['NEFT CR', 'IMPS CR', 'ACH C']):
                    df_categorized.loc[mask, 'Subcategory'] = 'Salary/Income Transfer'
                else:
                    df_categorized.loc[mask, 'Subcategory'] = 'Other Income'
    
    # Handle UPI transactions more specifically
    upi_mask = df_categorized['Narration'].str.contains('UPI-', case=False, na=False)
    upi_uncategorized = upi_mask & (df_categorized['Category'] == 'Others')
    
    # For uncategorized UPI transactions, try to extract merchant name
    def extract_upi_merchant(narration):
        if pd.isna(narration):
            return 'Unknown'
        
        # Pattern: UPI-MERCHANT_NAME-...
        match = re.search(r'UPI-([^-]+)-', narration)
        if match:
            merchant = match.group(1).strip()
            return merchant
        return 'Unknown UPI'
    
    df_categorized.loc[upi_uncategorized, 'Subcategory'] = df_categorized.loc[upi_uncategorized, 'Narration'].apply(extract_upi_merchant)
    
    # Add transaction type
    df_categorized['Transaction_Type'] = 'Debit'
    credit_mask = df_categorized['Deposit Amt.'].notna()
    df_categorized.loc[credit_mask, 'Transaction_Type'] = 'Credit'
    
    # Add amount column (unified)
    df_categorized['Amount'] = df_categorized['Withdrawal Amt.'].fillna(0) + df_categorized['Deposit Amt.'].fillna(0)
    
    return df_categorized

def generate_category_summary(df_categorized):
    """
    Generate summary statistics by category
    """
    print("=== TRANSACTION CATEGORIZATION SUMMARY ===\n")
    
    # Overall summary
    total_transactions = len(df_categorized)
    total_debits = df_categorized[df_categorized['Transaction_Type'] == 'Debit']['Amount'].sum()
    total_credits = df_categorized[df_categorized['Transaction_Type'] == 'Credit']['Amount'].sum()
    
    print(f"Total Transactions: {total_transactions}")
    print(f"Total Debits: ₹{total_debits:,.2f}")
    print(f"Total Credits: ₹{total_credits:,.2f}")
    print(f"Net Amount: ₹{total_credits - total_debits:,.2f}")
    print()
    
    # Category-wise breakdown
    print("Category-wise Breakdown:")
    print("-" * 60)
    
    category_summary = df_categorized.groupby(['Category', 'Transaction_Type']).agg({
        'Amount': ['sum', 'count'],
        'Date': ['min', 'max']
    }).round(2)
    
    for category in df_categorized['Category'].unique():
        cat_data = df_categorized[df_categorized['Category'] == category]
        debit_amount = cat_data[cat_data['Transaction_Type'] == 'Debit']['Amount'].sum()
        credit_amount = cat_data[cat_data['Transaction_Type'] == 'Credit']['Amount'].sum()
        transaction_count = len(cat_data)
        
        print(f"{category}:")
        print(f"  Debits: ₹{debit_amount:,.2f} | Credits: ₹{credit_amount:,.2f} | Count: {transaction_count}")
        
        # Top subcategories
        if transaction_count > 0:
            top_subcats = cat_data.groupby('Subcategory')['Amount'].sum().sort_values(ascending=False).head(3)
            print(f"  Top subcategories: {', '.join([f'{subcat} (₹{amt:,.0f})' for subcat, amt in top_subcats.items()])}")
        print()

def save_categorized_data(df_categorized, base_directory):
    """
    Save categorized data to Excel files in organized folders
    """
    import os
    
    # Create organized folder structure
    categorized_dir = os.path.join(base_directory, "Categorized_Files")
    periodic_dir = os.path.join(base_directory, "Periodic_Files")
    
    os.makedirs(categorized_dir, exist_ok=True)
    os.makedirs(periodic_dir, exist_ok=True)
    
    print(f"Creating organized folder structure...")
    print(f"  Categorized files: {categorized_dir}")
    print(f"  Periodic files: {periodic_dir}")
    
    # Save complete categorized data
    complete_file = os.path.join(categorized_dir, "Complete_Categorized_Statement.xlsx")
    df_categorized.to_excel(complete_file, index=False)
    print(f"Saved complete categorized data: {complete_file}")
    
    # Save category-wise files
    print("\nSaving category-wise files...")
    for category in df_categorized['Category'].unique():
        category_data = df_categorized[df_categorized['Category'] == category]
        safe_category_name = category.replace('&', 'and').replace('/', '_')
        category_file = os.path.join(categorized_dir, f"Category_{safe_category_name}.xlsx")
        category_data.to_excel(category_file, index=False)
        print(f"  Saved {category}: {len(category_data)} transactions")
    
    # Save monthly categorized data (separate files for each month)
    print("\nSaving monthly categorized files...")
    for month_year in df_categorized['Month_Year'].unique():
        month_data = df_categorized[df_categorized['Month_Year'] == month_year]
        month_file = os.path.join(periodic_dir, f"Monthly_Categorized_{month_year}.xlsx")
        month_data.to_excel(month_file, index=False)
        print(f"  Saved {month_year}: {len(month_data)} transactions")
    
    # Save monthly summary
    monthly_summary = df_categorized.groupby(['Month_Year', 'Category']).agg({
        'Amount': 'sum',
        'Date': 'count'
    }).reset_index()
    monthly_summary.columns = ['Month_Year', 'Category', 'Total_Amount', 'Transaction_Count']
    
    summary_file = os.path.join(periodic_dir, "Monthly_Category_Summary.xlsx")
    monthly_summary.to_excel(summary_file, index=False)
    print(f"Saved monthly summary: {summary_file}")
    
    # Create pivot table for better analysis
    pivot_summary = monthly_summary.pivot(index='Month_Year', columns='Category', values='Total_Amount').fillna(0)
    pivot_file = os.path.join(periodic_dir, "Monthly_Spending_Pivot.xlsx")
    pivot_summary.to_excel(pivot_file)
    print(f"Saved pivot analysis: {pivot_file}")

def main():
    # Load consolidated data from the new organized structure
    consolidated_file = 'Organized_Statements/Consolidated_Files/Complete_Consolidated_Statement.xlsx'
    
    # Check if the new structure exists, if not use old structure
    if not os.path.exists(consolidated_file):
        consolidated_file = 'Consolidated_Statements/Complete_Consolidated_Statement.xlsx'
        if not os.path.exists(consolidated_file):
            print("Error: No consolidated statement file found!")
            print("Please run the consolidation script first.")
            return
    
    df = pd.read_excel(consolidated_file)
    
    # Add Month_Year column for monthly analysis
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.to_period('M')
    
    print("Categorizing transactions...")
    df_categorized = categorize_transactions(df)
    
    # Generate summary
    generate_category_summary(df_categorized)
    
    # Save categorized data
    base_directory = "Organized_Statements"
    save_categorized_data(df_categorized, base_directory)
    
    print("\n=== CATEGORIZATION COMPLETE ===")
    print("Check the organized folder structure:")
    print("📁 Organized_Statements/")
    print("  📁 Monthly_Files/ (individual monthly Excel files)")
    print("  📁 Consolidated_Files/ (complete data and summaries)")
    print("  📁 Categorized_Files/ (category-wise Excel files)")
    print("    - Complete_Categorized_Statement.xlsx")
    print("    - Category_*.xlsx files")
    print("  📁 Periodic_Files/ (monthly analysis files)")
    print("    - Monthly_Categorized_*.xlsx files")
    print("    - Monthly_Category_Summary.xlsx")
    print("    - Monthly_Spending_Pivot.xlsx")

if __name__ == "__main__":
    main()
