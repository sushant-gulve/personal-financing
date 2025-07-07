import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob

class ImprovedSBIExtractor:
    def __init__(self):
        self.transactions = []
        
    def extract_text_with_password(self, pdf_path, password):
        """Extract text from password-protected PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            if doc.is_encrypted:
                if not doc.authenticate(password):
                    print(f"  Wrong password for {os.path.basename(pdf_path)}")
                    doc.close()
                    return None
            
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text() + "\n"
            
            doc.close()
            return text
            
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def parse_sbi_transactions_improved(self, text, filename):
        """Improved parsing specifically for SBI statement format"""
        lines = text.split('\n')
        transactions_found = 0
        
        # Look for the transaction table section
        in_transaction_section = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if we're entering transaction section
            if "Date" in line and "Credit" in line and "Debit" in line and "Balance" in line:
                in_transaction_section = True
                continue
            
            # Skip empty lines and headers
            if not line or line == "null":
                continue
                
            # Check if we're still in transaction section
            if in_transaction_section:
                # Parse SBI transaction format: DD-MM-YY Description - - Amount Balance
                # or DD-MM-YY Description Ref - Amount - Balance
                
                # Pattern for date at start of line
                date_match = re.match(r'^(\d{2}-\d{2}-\d{2})', line)
                if date_match:
                    date_str = date_match.group(1)
                    
                    # Convert YY to YYYY (assuming 20xx for years 00-30, 19xx for 31-99)
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
                    
                    # Look for the next few lines to get complete transaction info
                    transaction_lines = [line]
                    
                    # Collect related lines (description might span multiple lines)
                    j = i + 1
                    while j < len(lines) and j < i + 5:  # Look ahead max 5 lines
                        next_line = lines[j].strip()
                        if next_line and not re.match(r'^\d{2}-\d{2}-\d{2}', next_line):
                            transaction_lines.append(next_line)
                        else:
                            break
                        j += 1
                    
                    # Combine all transaction lines
                    full_transaction = ' '.join(transaction_lines)
                    
                    # Extract amounts from the combined transaction
                    amounts = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', full_transaction)
                    
                    if len(amounts) >= 2:
                        # Last amount is balance, check for debit/credit
                        balance = float(amounts[-1].replace(',', ''))
                        
                        # Look for credit and debit amounts
                        credit_amount = 0.0
                        debit_amount = 0.0
                        
                        # Check if there are separate credit/debit columns
                        if len(amounts) >= 3:
                            # Format: Description - CreditAmount DebitAmount Balance
                            # or Description Ref CreditAmount DebitAmount Balance
                            try:
                                potential_credit = amounts[-3]
                                potential_debit = amounts[-2]
                                
                                # Check context around amounts to determine which is credit/debit
                                if potential_credit != '-' and potential_credit != '0.00':
                                    credit_amount = float(potential_credit.replace(',', ''))
                                if potential_debit != '-' and potential_debit != '0.00':
                                    debit_amount = float(potential_debit.replace(',', ''))
                                    
                            except (ValueError, IndexError):
                                # Fall back to single amount
                                if len(amounts) >= 2:
                                    amount = float(amounts[-2].replace(',', ''))
                                    # Determine type based on description
                                    if '/DR/' in full_transaction or 'DEBIT' in full_transaction.upper():
                                        debit_amount = amount
                                    else:
                                        credit_amount = amount
                        else:
                            # Single amount, determine type from description
                            amount = float(amounts[-2].replace(',', ''))
                            if '/DR/' in full_transaction or 'DEBIT' in full_transaction.upper():
                                debit_amount = amount
                            else:
                                credit_amount = amount
                        
                        # Extract description (remove date and amounts)
                        description = full_transaction
                        # Remove date
                        description = re.sub(r'^\d{2}-\d{2}-\d{2}', '', description)
                        # Remove amounts
                        for amt in amounts:
                            description = description.replace(amt, '')
                        # Remove dashes and clean up
                        description = re.sub(r'-+', '', description)
                        description = re.sub(r'\s+', ' ', description).strip()
                        
                        # Create transaction record
                        if credit_amount > 0:
                            transaction = {
                                'Date': transaction_date,
                                'Description': description,
                                'Type': 'Credit',
                                'Amount': credit_amount,
                                'Balance': balance,
                                'Source_File': filename
                            }
                            self.transactions.append(transaction)
                            transactions_found += 1
                        
                        if debit_amount > 0:
                            transaction = {
                                'Date': transaction_date,
                                'Description': description,
                                'Type': 'Debit',
                                'Amount': debit_amount,
                                'Balance': balance,
                                'Source_File': filename
                            }
                            self.transactions.append(transaction)
                            transactions_found += 1
        
        return transactions_found
    
    def process_single_pdf(self, pdf_path, password):
        """Process a single PDF file"""
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}")
        
        text = self.extract_text_with_password(pdf_path, password)
        
        if not text:
            return 0
        
        transactions_found = self.parse_sbi_transactions_improved(text, filename)
        print(f"  Extracted {transactions_found} transactions")
        
        # Save sample if no transactions found
        if transactions_found == 0:
            sample_file = f"debug_{filename.replace('.pdf', '.txt')}"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  No transactions found. Full text saved to {sample_file}")
        
        return transactions_found
    
    def export_to_excel(self, output_path):
        """Export transactions to Excel"""
        if not self.transactions:
            print("No transactions found to export!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.transactions)
        
        # Sort by date
        df = df.sort_values('Date')
        
        # Format date column
        df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main transactions sheet
            df.to_excel(writer, sheet_name='All_Transactions', index=False)
            
            # Summary by month
            df_copy = df.copy()
            df_copy['Date'] = pd.to_datetime(df_copy['Date'], format='%d/%m/%Y')
            df_copy['Month'] = df_copy['Date'].dt.to_period('M')
            
            monthly_summary = df_copy.groupby(['Month', 'Type']).agg({
                'Amount': ['sum', 'count']
            }).round(2)
            monthly_summary.to_excel(writer, sheet_name='Monthly_Summary')
            
            # Summary by type
            type_summary = df.groupby('Type').agg({
                'Amount': ['sum', 'count', 'mean']
            }).round(2)
            type_summary.to_excel(writer, sheet_name='Type_Summary')
            
            # Format main sheet
            workbook = writer.book
            worksheet = writer.sheets['All_Transactions']
            
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
        
        print(f"Exported {len(self.transactions)} transactions to {output_path}")
        
        # Print summary
        credit_total = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Credit')
        debit_total = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Debit')
        
        print(f"\nTransaction Summary:")
        print(f"Total Credits: ₹{credit_total:,.2f}")
        print(f"Total Debits: ₹{debit_total:,.2f}")
        print(f"Net Amount: ₹{credit_total - debit_total:,.2f}")
        
        # Date range
        if self.transactions:
            dates = [t['Date'] for t in self.transactions]
            min_date = min(dates)
            max_date = max(dates)
            print(f"Date Range: {min_date.strftime('%d/%m/%Y')} to {max_date.strftime('%d/%m/%Y')}")
        
        # Transaction type breakdown
        credit_count = sum(1 for t in self.transactions if t['Type'] == 'Credit')
        debit_count = sum(1 for t in self.transactions if t['Type'] == 'Debit')
        print(f"Credit Transactions: {credit_count}")
        print(f"Debit Transactions: {debit_count}")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get password from user
    print("SBI Statement Transaction Extractor - Improved Version")
    print("=" * 55)
    password = input("Enter PDF password: ")
    
    if not password:
        print("Password is required. Exiting.")
        return
    
    extractor = ImprovedSBIExtractor()
    
    # Try statements folder first, then current directory
    statements_dir = os.path.join(current_dir, "statements")
    if os.path.exists(statements_dir):
        pdf_files = glob.glob(os.path.join(statements_dir, "*.pdf"))
        search_dir = statements_dir
        print(f"\nUsing statements folder: {statements_dir}")
    else:
        pdf_files = glob.glob(os.path.join(current_dir, "*.pdf"))
        search_dir = current_dir
        print(f"\nUsing current directory: {current_dir}")
    
    print(f"\nFound {len(pdf_files)} PDF files to process...")
    
    total_transactions = 0
    processed_files = 0
    
    for pdf_file in pdf_files:
        transactions = extractor.process_single_pdf(pdf_file, password)
        if transactions > 0:
            processed_files += 1
        total_transactions += transactions
    
    print(f"\nProcessing Complete!")
    print(f"Files processed successfully: {processed_files}/{len(pdf_files)}")
    print(f"Total transactions extracted: {total_transactions}")
    
    if total_transactions > 0:
        output_file = os.path.join(current_dir, "SBI_Transactions_Improved.xlsx")
        extractor.export_to_excel(output_file)
        print(f"\nExcel file created: {output_file}")
    else:
        print("\nNo transactions found. Please check:")
        print("1. Password is correct")
        print("2. PDF files are in 'statements' folder or current directory")
        print("3. PDF files are SBI bank statements")
        print("4. Check debug_*.txt files for text extraction issues")
        if 'search_dir' in locals():
            print(f"5. Searched in: {search_dir}")

if __name__ == "__main__":
    main()
