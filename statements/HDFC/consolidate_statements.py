import pandas as pd
import os
from datetime import datetime
import glob

def read_excel_files(directory_path):
    """Read all Excel files in the directory and return a list of DataFrames"""
    excel_files = glob.glob(os.path.join(directory_path, "*.xls*"))
    dataframes = []
    
    print(f"Found {len(excel_files)} Excel files:")
    for file in excel_files:
        print(f"  - {os.path.basename(file)}")
    
    for file_path in excel_files:
        try:
            # Try reading with different engines
            try:
                df = pd.read_excel(file_path, engine='xlrd')
            except:
                df = pd.read_excel(file_path, engine='openpyxl')
            
            # Add source file column
            df['Source_File'] = os.path.basename(file_path)
            dataframes.append(df)
            print(f"Successfully read {os.path.basename(file_path)} - {len(df)} rows")
            
        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {str(e)}")
    
    return dataframes

def identify_date_column(df):
    """Try to identify the date column in the DataFrame"""
    date_columns = []
    
    for col in df.columns:
        if any(word in str(col).lower() for word in ['date', 'transaction', 'time', 'posting']):
            # Check if this column contains date-like values
            try:
                pd.to_datetime(df[col].dropna().iloc[0])
                date_columns.append(col)
            except:
                pass
    
    return date_columns

def consolidate_and_organize_by_month(dataframes):
    """Consolidate DataFrames and organize by month"""
    if not dataframes:
        print("No dataframes to consolidate")
        return {}
    
    # Concatenate all dataframes
    consolidated_df = pd.concat(dataframes, ignore_index=True)
    print(f"Total consolidated records: {len(consolidated_df)}")
    
    # Display column information
    print("\nColumns in consolidated data:")
    for i, col in enumerate(consolidated_df.columns):
        print(f"  {i}: {col}")
    
    # Try to identify date columns
    date_columns = identify_date_column(consolidated_df)
    print(f"\nPotential date columns found: {date_columns}")
    
    if not date_columns:
        print("No date columns automatically detected. Please specify the date column manually.")
        return {'all_data': consolidated_df}
    
    # Use the first date column found
    date_col = date_columns[0]
    print(f"Using '{date_col}' as the date column")
    
    try:
        # Convert to datetime with explicit DD/MM/YY format
        consolidated_df[date_col] = pd.to_datetime(consolidated_df[date_col], format='%d/%m/%y', dayfirst=True)
        
        # Validate dates - check for any dates that seem incorrect
        current_date = datetime.now()
        future_dates = consolidated_df[consolidated_df[date_col] > current_date]
        if len(future_dates) > 0:
            print(f"\nWarning: Found {len(future_dates)} transactions with future dates:")
            print(future_dates[[date_col, 'Narration', 'Source_File']].head())
            print("This might indicate a date parsing issue.")
        
        # Show date range
        min_date = consolidated_df[date_col].min()
        max_date = consolidated_df[date_col].max()
        print(f"\nDate range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
        
        # Create month-year column
        consolidated_df['Month_Year'] = consolidated_df[date_col].dt.to_period('M')
        
        # Group by month
        monthly_data = {}
        for month_year, group in consolidated_df.groupby('Month_Year'):
            monthly_data[str(month_year)] = group.drop('Month_Year', axis=1)
            print(f"Month {month_year}: {len(group)} records")
        
        return monthly_data
    
    except Exception as e:
        print(f"Error processing dates: {str(e)}")
        return {'all_data': consolidated_df}

def save_monthly_data(monthly_data, base_directory):
    """Save monthly data to separate Excel files in organized folders"""
    import os
    
    # Create organized folder structure
    monthly_dir = os.path.join(base_directory, "Monthly_Files")
    consolidated_dir = os.path.join(base_directory, "Consolidated_Files")
    
    os.makedirs(monthly_dir, exist_ok=True)
    os.makedirs(consolidated_dir, exist_ok=True)
    
    print(f"\nCreating organized folder structure...")
    print(f"  Monthly files: {monthly_dir}")
    print(f"  Consolidated files: {consolidated_dir}")
    
    # Save monthly files
    print("\nSaving monthly statement files...")
    for month, data in monthly_data.items():
        filename = f"Statement_{month}.xlsx"
        filepath = os.path.join(monthly_dir, filename)
        
        try:
            data.to_excel(filepath, index=False)
            print(f"  Saved {filename}: {len(data)} records")
        except Exception as e:
            print(f"  Error saving {filename}: {str(e)}")
    
    # Save complete consolidated file
    if monthly_data:
        all_data = pd.concat(monthly_data.values(), ignore_index=True)
        complete_file = os.path.join(consolidated_dir, "Complete_Consolidated_Statement.xlsx")
        all_data.to_excel(complete_file, index=False)
        print(f"Saved complete consolidated file: {complete_file}")
        
        # Create a summary file
        summary_data = []
        for month, data in monthly_data.items():
            total_withdrawals = data['Withdrawal Amt.'].sum()
            total_deposits = data['Deposit Amt.'].sum()
            summary_data.append({
                'Month': month,
                'Total_Records': len(data),
                'Total_Withdrawals': total_withdrawals,
                'Total_Deposits': total_deposits,
                'Net_Amount': total_deposits - total_withdrawals
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_file = os.path.join(consolidated_dir, "Monthly_Summary.xlsx")
        summary_df.to_excel(summary_file, index=False)
        print(f"Saved monthly summary: {summary_file}")

def main():
    # Set the directory path
    directory_path = r"c:\Users\SG2952\Desktop\projects\personal financing\statements\HDFC"
    base_directory = os.path.join(directory_path, "Organized_Statements")
    
    print("=== HDFC Statement Consolidation ===")
    print(f"Reading files from: {directory_path}")
    print(f"Output directory: {base_directory}")
    print()
    
    # Read all Excel files
    dataframes = read_excel_files(directory_path)
    
    if not dataframes:
        print("No Excel files found or readable.")
        return
    
    # Show sample of first dataframe to understand structure
    print("\nSample data from first file:")
    print(dataframes[0].head())
    print("\nColumn details:")
    print(dataframes[0].info())
    
    # Consolidate and organize by month
    monthly_data = consolidate_and_organize_by_month(dataframes)
    
    # Save consolidated data
    print(f"\nSaving organized data to: {base_directory}")
    save_monthly_data(monthly_data, base_directory)
    
    print("\n=== CONSOLIDATION COMPLETE ===")
    print("Check the organized folder structure:")
    print("📁 Organized_Statements/")
    print("  📁 Monthly_Files/ (individual monthly Excel files)")
    print("  📁 Consolidated_Files/ (complete data and summaries)")

if __name__ == "__main__":
    main()
