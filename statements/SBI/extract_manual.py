import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob

class ManualSBIExtractor:
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
    
    def parse_sbi_transactions(self, text, filename):
        """Parse SBI statement text to extract transactions"""
        lines = text.split('\n')
        transactions_found = 0
        
        # Common transaction keywords to identify relevant lines
        transaction_keywords = [
            'NEFT', 'RTGS', 'IMPS', 'UPI', 'ATM', 'POS', 'CASH',
            'SALARY', 'DIVIDEND', 'INTEREST', 'CHARGES', 'FEES',
            'WITHDRAWAL', 'DEPOSIT', 'TRANSFER', 'PAYMENT',
            'DEBIT', 'CREDIT', 'REFUND', 'CHEQUE'
        ]
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 15:
                continue
            
            # Check if line contains transaction keywords
            if any(keyword in line.upper() for keyword in transaction_keywords):
                # Try to extract date (multiple formats)
                date_patterns = [
                    r'(\d{2}/\d{2}/\d{4})',
                    r'(\d{2}-\d{2}-\d{4})',
                    r'(\d{2}\.\d{2}\.\d{4})'
                ]
                
                date_found = None
                for pattern in date_patterns:
                    date_match = re.search(pattern, line)
                    if date_match:
                        date_str = date_match.group(1)
                        try:
                            if '/' in date_str:
                                date_found = datetime.strptime(date_str, '%d/%m/%Y')
                            elif '-' in date_str:
                                date_found = datetime.strptime(date_str, '%d-%m-%Y')
                            elif '.' in date_str:
                                date_found = datetime.strptime(date_str, '%d.%m.%Y')
                            break
                        except ValueError:
                            continue
                
                if not date_found:
                    continue
                
                # Extract amounts (numbers with decimal points)
                amounts = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                
                if len(amounts) >= 2:
                    # Usually: last is balance, second last is transaction amount
                    balance = float(amounts[-1].replace(',', ''))
                    amount = float(amounts[-2].replace(',', ''))
                    
                    # Clean description
                    description = line
                    for amt in amounts:
                        description = description.replace(amt, '')
                    for pattern in date_patterns:
                        description = re.sub(pattern, '', description)
                    description = re.sub(r'\s+', ' ', description).strip()
                    
                    # Remove common non-descriptive parts
                    description = re.sub(r'(DR|CR|DEBIT|CREDIT)', '', description, flags=re.IGNORECASE)
                    description = description.strip()
                    
                    # Determine transaction type
                    credit_indicators = ['SALARY', 'DIVIDEND', 'INTEREST', 'CREDIT', 'DEPOSIT', 'REFUND', 'CR']
                    debit_indicators = ['CHARGES', 'FEES', 'WITHDRAWAL', 'DEBIT', 'PAYMENT', 'ATM', 'POS', 'DR']
                    
                    transaction_type = 'Credit'
                    line_upper = line.upper()
                    
                    if any(indicator in line_upper for indicator in debit_indicators):
                        transaction_type = 'Debit'
                    elif any(indicator in line_upper for indicator in credit_indicators):
                        transaction_type = 'Credit'
                    else:
                        # Default logic: if amount is subtracted from balance, it's debit
                        # This is a simplified assumption
                        transaction_type = 'Debit'
                    
                    transaction = {
                        'Date': date_found,
                        'Description': description,
                        'Type': transaction_type,
                        'Amount': amount,
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
        
        transactions_found = self.parse_sbi_transactions(text, filename)
        print(f"  Extracted {transactions_found} transactions")
        
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
        
        # Create Excel file
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Transactions', index=False)
            
            # Auto-adjust column widths
            workbook = writer.book
            worksheet = writer.sheets['Transactions']
            
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

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get password from user
    print("SBI Statement Transaction Extractor")
    print("=" * 40)
    password = input("Enter PDF password: ")
    
    if not password:
        print("Password is required. Exiting.")
        return
    
    extractor = ManualSBIExtractor()
    
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
    for pdf_file in pdf_files:
        transactions = extractor.process_single_pdf(pdf_file, password)
        total_transactions += transactions
    
    print(f"\nTotal transactions extracted: {total_transactions}")
    
    if total_transactions > 0:
        output_file = os.path.join(current_dir, "SBI_Transactions_Final.xlsx")
        extractor.export_to_excel(output_file)
    else:
        print("No transactions found. Please check:")
        print("1. Password is correct")
        print("2. PDF files are in 'statements' folder or current directory")
        print("3. PDF files are SBI bank statements")
        print("4. PDF format matches SBI statement format")
        if 'search_dir' in locals():
            print(f"5. Searched in: {search_dir}")

if __name__ == "__main__":
    main()
