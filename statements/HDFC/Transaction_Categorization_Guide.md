# Transaction Categorization Strategy Guide

## Overview
This guide explains the automated transaction categorization system for your HDFC bank statements. The system has successfully categorized 719 transactions across 12 major categories.

## Financial Summary
- **Total Transactions**: 719
- **Total Debits**: ₹11,28,631.99
- **Total Credits**: ₹11,30,323.91
- **Net Amount**: ₹1,691.92 (Positive balance)

## Category Breakdown

### 1. **Banking & Finance** (151 transactions)
- **Amount**: ₹4,46,791.79 debits | ₹6,066.00 credits
- **Includes**: Bank charges, trading, investments, dividends, interest
- **Key Subcategories**:
  - Banking Services: ₹2,54,842
  - Trading/Investment: ₹1,97,414 (Zerodha transactions)
  - Bank Interest: ₹602

### 2. **Others** (383 transactions)
- **Amount**: ₹4,58,332.10 debits | ₹10,28,517.00 credits
- **Note**: Largest category - needs further refinement
- **Includes**: Unclassified UPI transactions, personal transfers

### 3. **Income & Salary** (24 transactions)
- **Amount**: ₹0.00 debits | ₹81,360.90 credits
- **Includes**: NEFT credits, salary transfers, income deposits
- **Key Subcategories**:
  - Salary/Income Transfer: ₹80,305
  - Other Income: ₹1,056

### 4. **Investments & Savings** (25 transactions)
- **Amount**: ₹63,870.71 debits | ₹170.00 credits
- **Includes**: Mutual funds, FDs, recurring deposits, SIP

### 5. **Shopping & Retail** (24 transactions)
- **Amount**: ₹46,432.52 debits | ₹0.00 credits
- **Includes**: Clothing, sports goods, general shopping
- **Key Merchants**: Decathlon, Parkar Shirts, various retail stores

### 6. **Cash & ATM** (7 transactions)
- **Amount**: ₹36,280.00 debits | ₹1.01 credits
- **Includes**: ATM withdrawals, cash transactions

### 7. **Utilities & Bills** (23 transactions)
- **Amount**: ₹35,006.00 debits | ₹4,000.00 credits
- **Includes**: Mobile, internet, electricity, water, gas bills

### 8. **Entertainment & Subscriptions** (7 transactions)
- **Amount**: ₹15,249.00 debits | ₹2.00 credits
- **Includes**: Spotify, Netflix, LinkedIn, Udemy, entertainment

### 9. **Transportation** (13 transactions)
- **Amount**: ₹11,753.00 debits | ₹10,199.00 credits
- **Includes**: Fuel, taxi, travel expenses

### 10. **Technology & Software** (35 transactions)
- **Amount**: ₹10,170.22 debits | ₹8.00 credits
- **Includes**: Google Cloud, software subscriptions, tech purchases

### 11. **Food & Dining** (15 transactions)
- **Amount**: ₹3,365.65 debits | ₹0.00 credits
- **Includes**: Zomato, Swiggy, restaurant payments
- **Key Subcategories**:
  - Online Food Delivery: ₹2,514
  - Restaurant/Local Food: ₹852

### 12. **Healthcare** (12 transactions)
- **Amount**: ₹1,381.00 debits | ₹0.00 credits
- **Includes**: Medical expenses, pharmacy, healthcare

## Generated Files

The categorization system has created the following files in the `Consolidated_Statements` folder:

### 1. **Main Files**
- `Categorized_Complete_Statement.xlsx` - All 719 transactions with categories
- `Monthly_Category_Summary.xlsx` - Monthly spending breakdown by category

### 2. **Category-wise Files**
- `Category_Banking and Finance.xlsx`
- `Category_Others.xlsx`
- `Category_Income and Salary.xlsx`
- `Category_Investments and Savings.xlsx`
- `Category_Shopping and Retail.xlsx`
- `Category_Cash and ATM.xlsx`
- `Category_Utilities and Bills.xlsx`
- `Category_Entertainment and Subscriptions.xlsx`
- `Category_Transportation.xlsx`
- `Category_Technology and Software.xlsx`
- `Category_Food and Dining.xlsx`
- `Category_Healthcare.xlsx`

## How to Use

### 1. **Running the Categorization**
- Double-click `run_categorization.bat` to automatically categorize new transactions
- Or run in terminal: `& ".\.venv\Scripts\python.exe" categorize_transactions.py`

### 2. **Analyzing Your Spending**
- Open `Categorized_Complete_Statement.xlsx` for complete view
- Use `Monthly_Category_Summary.xlsx` for monthly trends
- Open individual category files to analyze specific spending areas

### 3. **Customizing Categories**
Edit the `categorize_transactions.py` file to:
- Add new categories
- Modify existing category rules
- Add specific merchant mappings
- Adjust keyword matching

## Key Insights from Your Data

### **Spending Patterns**
1. **Largest Expenses**: Banking & Finance (₹4.47L) - mostly trading/investments
2. **Daily Expenses**: Shopping & Retail (₹46K), Utilities (₹35K)
3. **Regular Income**: ₹81K in salary/income credits
4. **Investment Activity**: ₹64K in investment transactions

### **Areas for Improvement**
1. **"Others" Category**: 383 transactions need better classification
2. **UPI Merchant Identification**: Many UPI transactions can be better categorized
3. **Monthly Budgeting**: Use monthly summaries to track spending trends

## Next Steps

### **Immediate Actions**
1. Review the "Others" category for manual classification
2. Add specific merchant names to improve future categorization
3. Set up monthly budget limits based on category spending

### **Advanced Features**
1. **Budget Tracking**: Set limits for each category
2. **Trend Analysis**: Compare month-over-month spending
3. **Savings Goals**: Track progress toward financial goals
4. **Expense Alerts**: Get notified when spending exceeds limits

## Maintenance

### **Regular Tasks**
1. Run categorization monthly after consolidating new statements
2. Review and update category rules quarterly
3. Add new merchant patterns as they appear
4. Analyze spending trends and adjust budgets

### **Custom Modifications**
The categorization rules can be easily modified by editing the `categories` dictionary in `categorize_transactions.py`. Add new keywords or categories as needed for your specific spending patterns.

---

**Last Updated**: July 7, 2025  
**Total Transactions Processed**: 719  
**Date Range**: April 2024 - July 2025
