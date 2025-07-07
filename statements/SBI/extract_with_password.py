import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob
import getpass

class PasswordProtectedSBIExtractor:
    def __init__(self):
        self.transactions = []
        self.failed_files = []
        self.password = None
        
    def get_password(self):
        """Get password from user"""
        if not self.password:
            print("Your PDF files are password-protected.")
            print("Common passwords for SBI statements:")
            print("1. Your date of birth (DDMMYYYY)")
            print("2. Your account number")
            print("3. Your mobile number")
            print("4. Your PAN number")
            print()
            
            self.password = getpass.getpass("Please enter the PDF password: ")
            
            # If user presses Enter without typing, try common formats
            if not self.password:
                print("No password entered. Please try again.")
                return False
        
        return True
    
    def extract_text_with_password(self, pdf_path):
        """Extract text from password-protected PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            if doc.is_encrypted:
                # Try to authenticate with password
                if not doc.authenticate(self.password):
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
            print(f"  Error processing {os.path.basename(pdf_path)}: {e}")
            return None
    
    def parse_sbi_transactions(self, text, filename):
        """Parse SBI statement text to extract transactions"""
        lines = text.split('\n')
        transactions_found = 0
        
        # Multiple patterns to match different SBI statement formats
        patterns = [
            # Pattern 1: DD/MM/YYYY Description Amount Balance
            r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(?:(DR|CR)\s+)?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            # Pattern 2: DD-MM-YYYY Description Amount Balance  
            r'(\d{2}-\d{2}-\d{4})\s+(.+?)\s+(?:(DR|CR)\s+)?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            # Pattern 3: With debit/credit columns
            r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        ]
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 15:
                continue
                
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    
                    # Extract date
                    date_str = groups[0]
                    try:
                        if '/' in date_str:
                            transaction_date = datetime.strptime(date_str, '%d/%m/%Y')
                        else:
                            transaction_date = datetime.strptime(date_str, '%d-%m-%Y')
                    except ValueError:
                        continue
                    
                    # Extract description
                    description = groups[1].strip()
                    
                    # Handle different group structures
                    if len(groups) == 5:  # Date, Description, DR/CR, Amount, Balance
                        dr_cr = groups[2]
                        amount = float(groups[3].replace(',', ''))
                        balance = float(groups[4].replace(',', ''))
                        transaction_type = 'Credit' if dr_cr == 'CR' else 'Debit'
                    elif len(groups) == 6:  # Date, Description, Debit, Credit, Balance
                        debit_amt = groups[2]
                        credit_amt = groups[3]
                        balance = float(groups[4].replace(',', ''))
                        
                        if debit_amt and debit_amt.replace(',', '').replace('.', '').isdigit():
                            amount = float(debit_amt.replace(',', ''))
                            transaction_type = 'Debit'
                        else:
                            amount = float(credit_amt.replace(',', ''))
                            transaction_type = 'Credit'
                    else:
                        continue
                    
                    # Clean description
                    description = re.sub(r'\s+', ' ', description).strip()
                    
                    # Skip if description is too short or contains only numbers
                    if len(description) < 3 or description.isdigit():
                        continue
                    
                    transaction = {
                        'Date': transaction_date,
                        'Description': description,
                        'Type': transaction_type,
                        'Amount': amount,
                        'Balance': balance,
                        'Source_File': filename
                    }
                    
                    self.transactions.append(transaction)
                    transactions_found += 1
                    break
        
        return transactions_found
    
    def extract_transaction_summary(self, text):
        """Extract transaction summary information"""
        # Look for opening/closing balance
        opening_balance = None
        closing_balance = None
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip().upper()
            if 'OPENING BALANCE' in line:
                balance_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                if balance_match:
                    opening_balance = float(balance_match.group(1).replace(',', ''))
            elif 'CLOSING BALANCE' in line:
                balance_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                if balance_match:
                    closing_balance = float(balance_match.group(1).replace(',', ''))
        
        return opening_balance, closing_balance
    
    def process_pdf(self, pdf_path):
        """Process a single PDF file"""
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}")
        
        # Extract text
        text = self.extract_text_with_password(pdf_path)
        
        if not text:
            self.failed_files.append(filename)
            return
        
        # Parse transactions
        transactions_found = self.parse_sbi_transactions(text, filename)
        
        if transactions_found == 0:
            # Save sample text for manual inspection
            sample_file = f"sample_{filename.replace('.pdf', '.txt')}"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(text[:3000])  # First 3000 characters
            print(f"  No transactions found. Sample text saved to {sample_file}")
        
        print(f"  Extracted {transactions_found} transactions")
    
    def process_all_pdfs(self, directory_path):
        """Process all PDF files"""
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        
        print(f"Found {len(pdf_files)} PDF files to process...")
        
        # Get password once
        if not self.get_password():
            return
        
        for pdf_file in pdf_files:
            self.process_pdf(pdf_file)
    
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
            df_monthly = df.copy()
            df_monthly['Month'] = pd.to_datetime(df_monthly['Date'], format='%d/%m/%Y').dt.to_period('M')
            monthly_summary = df_monthly.groupby(['Month', 'Type']).agg({
                'Amount': ['sum', 'count']
            }).round(2)
            monthly_summary.to_excel(writer, sheet_name='Monthly_Summary')
            
            # Summary by file
            file_summary = df.groupby('Source_File').agg({
                'Amount': 'count',
                'Type': lambda x: f"Credits: {sum(x == 'Credit')}, Debits: {sum(x == 'Debit')}"
            })
            file_summary.to_excel(writer, sheet_name='File_Summary')
            
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
                adjusted_width = min(max_length + 2, 50)
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
        
        if self.failed_files:
            print(f"\nFailed to process {len(self.failed_files)} files:")
            for file in self.failed_files:
                print(f"  - {file}")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    extractor = PasswordProtectedSBIExtractor()
    
    # Try statements folder first, then current directory
    statements_dir = os.path.join(current_dir, "statements")
    if os.path.exists(statements_dir):
        search_dir = statements_dir
        print(f"Using statements folder: {statements_dir}")
    else:
        search_dir = current_dir
        print(f"Using current directory: {current_dir}")
    
    extractor.process_all_pdfs(search_dir)
    
    output_file = os.path.join(current_dir, "SBI_Transactions_Complete.xlsx")
    extractor.export_to_excel(output_file)

if __name__ == "__main__":
    main()
