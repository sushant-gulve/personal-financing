import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob
from collections import defaultdict

class ConsolidatedSBIExtractor:
    def __init__(self):
        self.transactions = []
        self.file_summary = defaultdict(int)
        self.monthly_summary = defaultdict(lambda: {'credits': 0, 'debits': 0, 'count': 0})
        
    def extract_text_with_password(self, pdf_path, password):
        """Extract text from password-protected PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            if doc.is_encrypted:
                if not doc.authenticate(password):
                    print(f"  ❌ Wrong password for {os.path.basename(pdf_path)}")
                    doc.close()
                    return None
            
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text() + "\n"
            
            doc.close()
            return text
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None
    
    def parse_sbi_transactions_consolidated(self, text, filename):
        """Parse SBI transactions and build consolidated data"""
        lines = text.split('\n')
        transactions_found = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Match SBI transaction format: DD-MM-YY at start
            date_match = re.match(r'^(\d{2}-\d{2}-\d{2})', line)
            if date_match:
                date_str = date_match.group(1)
                
                # Convert YY to YYYY
                day, month, year = date_str.split('-')
                year_int = int(year)
                if year_int <= 30:
                    full_year = 2000 + year_int
                else:
                    full_year = 1900 + year_int
                
                try:
                    transaction_date = datetime(full_year, int(month), int(day))
                except ValueError:
                    continue
                
                # Collect transaction lines
                transaction_parts = []
                j = i
                while j < len(lines) and j < i + 6:
                    current_line = lines[j].strip()
                    if current_line:
                        transaction_parts.append(current_line)
                    j += 1
                    
                    # Check for complete transaction
                    combined_text = ' '.join(transaction_parts)
                    amounts = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', combined_text)
                    
                    if len(amounts) >= 2:
                        if j < len(lines) and re.match(r'^\d{2}-\d{2}-\d{2}', lines[j].strip()):
                            break
                        elif len(amounts) >= 3:
                            break
                
                # Process the transaction
                combined_transaction = ' '.join(transaction_parts)
                amounts = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', combined_transaction)
                
                if len(amounts) >= 2:
                    balance = float(amounts[-1].replace(',', ''))
                    
                    # Find transaction amount
                    transaction_amount = 0.0
                    for amount in amounts[:-1]:
                        amt_val = float(amount.replace(',', ''))
                        if amt_val > 0:
                            transaction_amount = amt_val
                            break
                    
                    # Extract description
                    description = combined_transaction
                    description = re.sub(r'^\d{2}-\d{2}-\d{2}', '', description)
                    for amt in amounts:
                        description = description.replace(amt, '')
                    description = re.sub(r'-+', ' ', description)
                    description = re.sub(r'\s+', ' ', description).strip()
                    
                    # Determine transaction type
                    if '/DR/' in combined_transaction:
                        transaction_type = 'Debit'
                    elif '/CR/' in combined_transaction:
                        transaction_type = 'Credit'
                    elif any(keyword in description.upper() for keyword in ['SALARY', 'DIVIDEND', 'INTEREST', 'DEPOSIT', 'CREDIT']):
                        transaction_type = 'Credit'
                    else:
                        transaction_type = 'Debit'
                    
                    if transaction_amount > 0:
                        # Add to consolidated transactions
                        transaction = {
                            'Date': transaction_date,
                            'Description': description,
                            'Type': transaction_type,
                            'Amount': transaction_amount,
                            'Balance': balance,
                            'Source_File': filename,
                            'Month': transaction_date.strftime('%Y-%m'),
                            'Year': transaction_date.year
                        }
                        
                        self.transactions.append(transaction)
                        transactions_found += 1
                        
                        # Update summaries
                        self.file_summary[filename] += 1
                        month_key = transaction_date.strftime('%Y-%m')
                        self.monthly_summary[month_key]['count'] += 1
                        if transaction_type == 'Credit':
                            self.monthly_summary[month_key]['credits'] += transaction_amount
                        else:
                            self.monthly_summary[month_key]['debits'] += transaction_amount
        
        return transactions_found
    
    def process_all_pdfs_consolidated(self, directory_path, password):
        """Process all PDFs and consolidate transactions"""
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        
        print(f"📁 Found {len(pdf_files)} PDF files to consolidate...")
        print("=" * 60)
        
        total_transactions = 0
        processed_files = 0
        failed_files = []
        
        for i, pdf_file in enumerate(pdf_files, 1):
            filename = os.path.basename(pdf_file)
            print(f"[{i}/{len(pdf_files)}] Processing: {filename}")
            
            text = self.extract_text_with_password(pdf_file, password)
            
            if text:
                transactions = self.parse_sbi_transactions_consolidated(text, filename)
                if transactions > 0:
                    processed_files += 1
                    print(f"  ✅ Extracted {transactions} transactions")
                else:
                    failed_files.append(filename)
                    print(f"  ⚠️  No transactions found")
                total_transactions += transactions
            else:
                failed_files.append(filename)
                print(f"  ❌ Failed to extract text")
        
        print("\n" + "=" * 60)
        print(f"🎉 Consolidation Complete!")
        print(f"✅ Files processed: {processed_files}/{len(pdf_files)}")
        print(f"📊 Total transactions: {total_transactions}")
        
        if failed_files:
            print(f"⚠️  Files with issues: {len(failed_files)}")
        
        return total_transactions > 0
    
    def export_consolidated_excel(self, output_path):
        """Export consolidated transactions to Excel with multiple sheets"""
        if not self.transactions:
            print("❌ No transactions found to export!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.transactions)
        df = df.sort_values(['Date', 'Source_File'])
        
        # Format date for Excel
        df['Date_Excel'] = df['Date'].dt.strftime('%d/%m/%Y')
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: All Transactions (Main consolidated view)
            export_df = df[['Date_Excel', 'Description', 'Type', 'Amount', 'Balance', 'Source_File']].copy()
            export_df.rename(columns={'Date_Excel': 'Date'}, inplace=True)
            export_df.to_excel(writer, sheet_name='All_Transactions', index=False)
            
            # Sheet 2: Monthly Summary
            monthly_data = []
            for month, data in sorted(self.monthly_summary.items()):
                monthly_data.append({
                    'Month': month,
                    'Total_Credits': data['credits'],
                    'Total_Debits': data['debits'],
                    'Net_Amount': data['credits'] - data['debits'],
                    'Transaction_Count': data['count']
                })
            
            monthly_df = pd.DataFrame(monthly_data)
            monthly_df.to_excel(writer, sheet_name='Monthly_Summary', index=False)
            
            # Sheet 3: File-wise Summary
            file_data = []
            for filename, count in self.file_summary.items():
                file_transactions = [t for t in self.transactions if t['Source_File'] == filename]
                credits = sum(t['Amount'] for t in file_transactions if t['Type'] == 'Credit')
                debits = sum(t['Amount'] for t in file_transactions if t['Type'] == 'Debit')
                
                file_data.append({
                    'File_Name': filename,
                    'Transaction_Count': count,
                    'Credits': credits,
                    'Debits': debits,
                    'Net_Amount': credits - debits
                })
            
            file_df = pd.DataFrame(file_data)
            file_df.to_excel(writer, sheet_name='File_Summary', index=False)
            
            # Sheet 4: Transaction Types
            type_summary = df.groupby('Type').agg({
                'Amount': ['sum', 'count', 'mean', 'min', 'max']
            }).round(2)
            type_summary.to_excel(writer, sheet_name='Transaction_Types')
            
            # Sheet 5: Yearly Summary
            yearly_summary = df.groupby('Year').agg({
                'Amount': ['sum', 'count'],
                'Type': lambda x: f"Credits: {sum(x == 'Credit')}, Debits: {sum(x == 'Debit')}"
            }).round(2)
            yearly_summary.to_excel(writer, sheet_name='Yearly_Summary')
            
            # Format all sheets
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 60)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✅ Consolidated Excel file created: {output_path}")
        
        # Print detailed summary
        self.print_consolidated_summary()
    
    def print_consolidated_summary(self):
        """Print detailed consolidated summary"""
        print("\n" + "=" * 60)
        print("📊 CONSOLIDATED TRANSACTION SUMMARY")
        print("=" * 60)
        
        # Overall totals
        total_credits = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Credit')
        total_debits = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Debit')
        
        print(f"💰 Total Credits: ₹{total_credits:,.2f}")
        print(f"💸 Total Debits: ₹{total_debits:,.2f}")
        print(f"📈 Net Amount: ₹{total_credits - total_debits:,.2f}")
        
        # Date range
        if self.transactions:
            dates = [t['Date'] for t in self.transactions]
            min_date = min(dates)
            max_date = max(dates)
            print(f"📅 Date Range: {min_date.strftime('%d/%m/%Y')} to {max_date.strftime('%d/%m/%Y')}")
        
        # Transaction counts
        credit_count = sum(1 for t in self.transactions if t['Type'] == 'Credit')
        debit_count = sum(1 for t in self.transactions if t['Type'] == 'Debit')
        print(f"📊 Total Transactions: {len(self.transactions)}")
        print(f"   • Credit Transactions: {credit_count}")
        print(f"   • Debit Transactions: {debit_count}")
        
        # Monthly breakdown (last 6 months)
        print(f"\n📅 Monthly Breakdown (Recent):")
        sorted_months = sorted(self.monthly_summary.keys(), reverse=True)
        for month in sorted_months[:6]:  # Last 6 months
            data = self.monthly_summary[month]
            net = data['credits'] - data['debits']
            print(f"   {month}: ₹{net:,.2f} (Credits: ₹{data['credits']:,.2f}, Debits: ₹{data['debits']:,.2f})")
        
        # File summary (top 5 files by transaction count)
        print(f"\n📁 Top Files by Transaction Count:")
        sorted_files = sorted(self.file_summary.items(), key=lambda x: x[1], reverse=True)
        for filename, count in sorted_files[:5]:
            print(f"   {filename}: {count} transactions")
        
        print("\n✨ Consolidation complete! Check the Excel file for detailed analysis.")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🏦 SBI CONSOLIDATED TRANSACTION EXTRACTOR")
    print("=" * 60)
    print("This will extract and consolidate ALL transactions from ALL PDF files")
    print("=" * 60)
    
    # Get password
    password = input("🔐 Enter PDF password: ")
    
    if not password:
        print("❌ Password is required. Exiting.")
        return
    
    # Create extractor and process all files
    extractor = ConsolidatedSBIExtractor()
    
    # Try statements folder first, then current directory
    statements_dir = os.path.join(current_dir, "statements")
    if os.path.exists(statements_dir):
        search_dir = statements_dir
        print(f"📁 Using statements folder: {statements_dir}")
    else:
        search_dir = current_dir
        print(f"📁 Using current directory: {current_dir}")
    
    success = extractor.process_all_pdfs_consolidated(search_dir, password)
    
    if success:
        output_file = os.path.join(current_dir, "SBI_Consolidated_Transactions.xlsx")
        extractor.export_consolidated_excel(output_file)
        
        print(f"\n🎉 SUCCESS! Your consolidated transactions are ready.")
        print(f"📁 File: {output_file}")
        print(f"📊 Sheets: All_Transactions, Monthly_Summary, File_Summary, Transaction_Types, Yearly_Summary")
        
    else:
        print("\n❌ No transactions found. Please check:")
        print("1. Password is correct")
        print("2. PDF files are in 'statements' folder or current directory") 
        print("3. PDF files are SBI bank statements")
        print(f"4. Searched in: {search_dir}")

if __name__ == "__main__":
    main()
