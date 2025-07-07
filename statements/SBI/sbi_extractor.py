#!/usr/bin/env python3
"""
SBI Transaction Extractor - Command Line Tool
Extracts transactions from SBI bank statement PDFs and organizes output in folders.
"""

import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob
import argparse
import sys
from pathlib import Path

class SBITransactionExtractor:
    def __init__(self, output_dir="extracted_transactions"):
        self.transactions = []
        self.output_dir = Path(output_dir)
        self.failed_files = []
        
        # Create output directory structure
        self.setup_output_directories()
    
    def setup_output_directories(self):
        """Create organized output directory structure"""
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "excel_files").mkdir(exist_ok=True)
        (self.output_dir / "debug_files").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        
        print(f"📁 Output directory created: {self.output_dir.absolute()}")
    
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
    
    def parse_sbi_transactions(self, text, filename):
        """Parse SBI transactions from text"""
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
                        transaction = {
                            'Date': transaction_date,
                            'Description': description,
                            'Type': transaction_type,
                            'Amount': transaction_amount,
                            'Balance': balance,
                            'Source_File': filename
                        }
                        
                        self.transactions.append(transaction)
                        transactions_found += 1
        
        return transactions_found
    
    def process_single_pdf(self, pdf_path, password):
        """Process a single PDF file"""
        filename = os.path.basename(pdf_path)
        print(f"📄 Processing: {filename}")
        
        text = self.extract_text_with_password(pdf_path, password)
        
        if not text:
            self.failed_files.append(filename)
            return 0
        
        transactions_found = self.parse_sbi_transactions(text, filename)
        print(f"  ✅ Extracted {transactions_found} transactions")
        
        # Save debug file if no transactions found
        if transactions_found == 0:
            debug_file = self.output_dir / "debug_files" / f"debug_{filename.replace('.pdf', '.txt')}"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  ⚠️  Debug file saved: {debug_file}")
        
        return transactions_found
    
    def export_to_excel(self):
        """Export transactions to Excel with organized structure"""
        if not self.transactions:
            print("❌ No transactions found to export!")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(self.transactions)
        df = df.sort_values('Date')
        
        # Format date column
        df['Date_Display'] = df['Date'].dt.strftime('%d/%m/%Y')
        
        # Create main Excel file
        main_excel = self.output_dir / "excel_files" / "SBI_All_Transactions.xlsx"
        
        with pd.ExcelWriter(main_excel, engine='openpyxl') as writer:
            # Main transactions sheet
            export_df = df[['Date_Display', 'Description', 'Type', 'Amount', 'Balance', 'Source_File']].copy()
            export_df.rename(columns={'Date_Display': 'Date'}, inplace=True)
            export_df.to_excel(writer, sheet_name='All_Transactions', index=False)
            
            # Monthly Summary
            df_monthly = df.copy()
            df_monthly['Month'] = df_monthly['Date'].dt.to_period('M')
            monthly_summary = df_monthly.groupby(['Month', 'Type']).agg({
                'Amount': ['sum', 'count']
            }).round(2)
            monthly_summary.to_excel(writer, sheet_name='Monthly_Summary')
            
            # File Summary
            file_summary = df.groupby('Source_File').agg({
                'Amount': ['count', 'sum'],
                'Type': lambda x: f"Credits: {sum(x == 'Credit')}, Debits: {sum(x == 'Debit')}"
            }).round(2)
            file_summary.to_excel(writer, sheet_name='File_Summary')
            
            # Format sheets
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
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
        
        # Create separate files by year
        years = df['Date'].dt.year.unique()
        for year in years:
            year_df = df[df['Date'].dt.year == year].copy()
            year_df['Date_Display'] = year_df['Date'].dt.strftime('%d/%m/%Y')
            
            year_excel = self.output_dir / "excel_files" / f"SBI_Transactions_{year}.xlsx"
            export_year_df = year_df[['Date_Display', 'Description', 'Type', 'Amount', 'Balance', 'Source_File']].copy()
            export_year_df.rename(columns={'Date_Display': 'Date'}, inplace=True)
            export_year_df.to_excel(year_excel, index=False)
        
        return main_excel
    
    def generate_report(self):
        """Generate summary report"""
        if not self.transactions:
            return None
        
        report_file = self.output_dir / "reports" / "summary_report.txt"
        
        # Calculate summary statistics
        total_credits = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Credit')
        total_debits = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Debit')
        credit_count = sum(1 for t in self.transactions if t['Type'] == 'Credit')
        debit_count = sum(1 for t in self.transactions if t['Type'] == 'Debit')
        
        dates = [t['Date'] for t in self.transactions]
        min_date = min(dates)
        max_date = max(dates)
        
        # Create monthly breakdown
        monthly_data = {}
        for transaction in self.transactions:
            month_key = transaction['Date'].strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {'credits': 0, 'debits': 0, 'count': 0}
            
            monthly_data[month_key]['count'] += 1
            if transaction['Type'] == 'Credit':
                monthly_data[month_key]['credits'] += transaction['Amount']
            else:
                monthly_data[month_key]['debits'] += transaction['Amount']
        
        # Write report
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("SBI TRANSACTION EXTRACTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Extraction Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total Transactions: {len(self.transactions)}\n")
            f.write(f"Date Range: {min_date.strftime('%d/%m/%Y')} to {max_date.strftime('%d/%m/%Y')}\n\n")
            
            f.write("FINANCIAL SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Credits: ₹{total_credits:,.2f} ({credit_count} transactions)\n")
            f.write(f"Total Debits: ₹{total_debits:,.2f} ({debit_count} transactions)\n")
            f.write(f"Net Amount: ₹{total_credits - total_debits:,.2f}\n\n")
            
            f.write("MONTHLY BREAKDOWN\n")
            f.write("-" * 20 + "\n")
            for month in sorted(monthly_data.keys()):
                data = monthly_data[month]
                net = data['credits'] - data['debits']
                f.write(f"{month}: ₹{net:,.2f} (C: ₹{data['credits']:,.2f}, D: ₹{data['debits']:,.2f}, Count: {data['count']})\n")
            
            f.write("\nFILE PROCESSING SUMMARY\n")
            f.write("-" * 25 + "\n")
            file_counts = {}
            for transaction in self.transactions:
                file_counts[transaction['Source_File']] = file_counts.get(transaction['Source_File'], 0) + 1
            
            for filename, count in sorted(file_counts.items()):
                f.write(f"{filename}: {count} transactions\n")
            
            if self.failed_files:
                f.write(f"\nFAILED FILES ({len(self.failed_files)})\n")
                f.write("-" * 15 + "\n")
                for filename in self.failed_files:
                    f.write(f"{filename}\n")
        
        return report_file
    
    def process_all_pdfs(self, directory_path, password):
        """Process all PDFs in directory"""
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        
        if not pdf_files:
            print("❌ No PDF files found in the directory!")
            return False
        
        print(f"📁 Found {len(pdf_files)} PDF files to process")
        print("=" * 60)
        
        total_transactions = 0
        processed_files = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}]", end=" ")
            transactions = self.process_single_pdf(pdf_file, password)
            if transactions > 0:
                processed_files += 1
            total_transactions += transactions
        
        print("\n" + "=" * 60)
        print(f"🎉 Processing Complete!")
        print(f"✅ Files processed: {processed_files}/{len(pdf_files)}")
        print(f"❌ Failed files: {len(self.failed_files)}")
        print(f"📊 Total transactions: {total_transactions}")
        
        return total_transactions > 0

def main():
    parser = argparse.ArgumentParser(description="Extract transactions from SBI bank statement PDFs")
    parser.add_argument("--input", "-i", default="statements", help="Input directory containing PDF files (default: statements)")
    parser.add_argument("--output", "-o", default="extracted_transactions", help="Output directory (default: extracted_transactions)")
    parser.add_argument("--password", "-p", help="PDF password (will prompt if not provided)")
    
    args = parser.parse_args()
    
    # Print header
    print("🏦 SBI TRANSACTION EXTRACTOR - COMMAND LINE TOOL")
    print("=" * 60)
    
    # Validate input directory - check both specified path and fallback to current directory
    input_dir = Path(args.input)
    if not input_dir.exists():
        # Try current directory as fallback
        fallback_dir = Path(".")
        pdf_files_in_current = list(fallback_dir.glob("*.pdf"))
        if pdf_files_in_current:
            print(f"⚠️  Input directory '{input_dir}' not found, using current directory with {len(pdf_files_in_current)} PDF files")
            input_dir = fallback_dir
        else:
            print(f"❌ Input directory does not exist: {input_dir}")
            print(f"💡 Make sure your PDF files are in a 'statements' folder or specify the correct path with --input")
            sys.exit(1)
    
    # Get password
    password = args.password
    if not password:
        password = input("🔐 Enter PDF password: ")
    
    if not password:
        print("❌ Password is required!")
        sys.exit(1)
    
    # Initialize extractor
    extractor = SBITransactionExtractor(args.output)
    
    # Process all PDFs
    success = extractor.process_all_pdfs(input_dir, password)
    
    if success:
        print("\n📊 Generating Excel files...")
        main_excel = extractor.export_to_excel()
        
        print("📋 Generating summary report...")
        report_file = extractor.generate_report()
        
        print(f"\n✅ SUCCESS! Extraction completed successfully.")
        print(f"📁 Output directory: {extractor.output_dir.absolute()}")
        print(f"📊 Main Excel file: {main_excel}")
        print(f"📋 Summary report: {report_file}")
        
        # Print quick summary
        total_credits = sum(t['Amount'] for t in extractor.transactions if t['Type'] == 'Credit')
        total_debits = sum(t['Amount'] for t in extractor.transactions if t['Type'] == 'Debit')
        
        print(f"\n💰 Total Credits: ₹{total_credits:,.2f}")
        print(f"💸 Total Debits: ₹{total_debits:,.2f}")
        print(f"📈 Net Amount: ₹{total_credits - total_debits:,.2f}")
        
    else:
        print("\n❌ No transactions found! Check your password and PDF files.")
        sys.exit(1)

if __name__ == "__main__":
    main()
