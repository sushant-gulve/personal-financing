import pandas as pd

# Load the consolidated data
df = pd.read_excel('Consolidated_Statements/Complete_Consolidated_Statement.xlsx')

print(f"Total transactions: {len(df)}")
print("\nSample narrations:")
for i, narration in enumerate(df['Narration'].head(15)):
    print(f"{i+1}. {narration}")

print("\nTransaction types breakdown:")
print(f"Withdrawals: {df['Withdrawal Amt.'].notna().sum()}")
print(f"Deposits: {df['Deposit Amt.'].notna().sum()}")

print("\nUnique narration patterns (first 20):")
unique_patterns = df['Narration'].str.split('-').str[0].unique()[:20]
for pattern in unique_patterns:
    print(f"- {pattern}")
