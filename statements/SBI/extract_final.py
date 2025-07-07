import os
import re
import pandas as pd
import fitz  # PyMuPDF
from datetime import datetime
import glob

class FinalSBIExtractor:
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
    
    def parse_sbi_transactions_final(self, text, filename):
        """Final improved parsing for SBI statements"""
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
                
                # Look for the complete transaction in next lines
                # SBI format: Date, Description, Reference, Credit, Debit, Balance
                transaction_parts = []
                current_line = line
                
                # Collect lines until we find the balance (last amount in the transaction)
                j = i
                while j < len(lines) and j < i + 6:  # Max 6 lines per transaction
                    current_line = lines[j].strip()
                    if current_line:
                        transaction_parts.append(current_line)
                    j += 1
                    
                    # Check if we have found a complete transaction
                    # Look for pattern: amounts ending with balance
                    combined_text = ' '.join(transaction_parts)
                    amounts = re.findall(r'\b(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b', combined_text)
                    
                    if len(amounts) >= 2:
                        # Check if next line starts with a date (new transaction)
                        if j < len(lines) and re.match(r'^\d{2}-\d{2}-\d{2}', lines[j].strip()):
                            break
                        # Or if we have enough amounts for a complete transaction
                        elif len(amounts) >= 3:
                            break
                
                # Process the collected transaction
                combined_transaction = ' '.join(transaction_parts)
                
                # Extract amounts - be more specific about decimal amounts
                amounts = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', combined_transaction)
                
                if len(amounts) >= 2:
                    # For SBI format: typically Credit, Debit, Balance
                    # or just Debit, Balance (when credit is -)
                    balance = float(amounts[-1].replace(',', ''))
                    
                    # Find the transaction amount
                    transaction_amount = 0.0
                    transaction_type = 'Debit'  # Default
                    
                    # Check the structure
                    if len(amounts) >= 2:
                        # Look for the actual transaction amount (not balance)
                        # Usually the second last amount
                        for amount in amounts[:-1]:  # All except balance
                            amt_val = float(amount.replace(',', ''))
                            if amt_val > 0:  # Valid transaction amount
                                transaction_amount = amt_val
                                break
                    
                    # Extract description (everything except date and amounts)
                    description = combined_transaction
                    
                    # Remove date
                    description = re.sub(r'^\d{2}-\d{2}-\d{2}', '', description)
                    
                    # Remove amounts
                    for amt in amounts:
                        description = description.replace(amt, '')
                    
                    # Remove dashes and clean up
                    description = re.sub(r'-+', ' ', description)
                    description = re.sub(r'\s+', ' ', description).strip()
                    
                    # Determine transaction type from description
                    if '/DR/' in combined_transaction:
                        transaction_type = 'Debit'
                    elif '/CR/' in combined_transaction:
                        transaction_type = 'Credit'
                    elif any(keyword in description.upper() for keyword in ['SALARY', 'DIVIDEND', 'INTEREST', 'DEPOSIT', 'CREDIT']):
                        transaction_type = 'Credit'
                    else:
                        transaction_type = 'Debit'  # Default for SBI
                    
                    # Only add if we have a valid amount
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
        print(f"Processing: {filename}")
        
        text = self.extract_text_with_password(pdf_path, password)
        
        if not text:
            return 0
        
        transactions_found = self.parse_sbi_transactions_final(text, filename)
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
            df.to_excel(writer, sheet_name='All_Transactions', index=False)
            
            # Format the sheet
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
        
        print(f"✅ Successfully exported {len(self.transactions)} transactions to {output_path}")
        
        # Print summary
        credit_total = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Credit')
        debit_total = sum(t['Amount'] for t in self.transactions if t['Type'] == 'Debit')
        
        print(f"\n📊 Transaction Summary:")
        print(f"💰 Total Credits: ₹{credit_total:,.2f}")
        print(f"💸 Total Debits: ₹{debit_total:,.2f}")
        print(f"📈 Net Amount: ₹{credit_total - debit_total:,.2f}")
        
        # Date range
        if self.transactions:
            dates = [t['Date'] for t in self.transactions]
            min_date = min(dates)
            max_date = max(dates)
            print(f"📅 Date Range: {min_date.strftime('%d/%m/%Y')} to {max_date.strftime('%d/%m/%Y')}")
        
        # Transaction counts
        credit_count = sum(1 for t in self.transactions if t['Type'] == 'Credit')
        debit_count = sum(1 for t in self.transactions if t['Type'] == 'Debit')
        print(f"📊 Credit Transactions: {credit_count}")
        print(f"📊 Debit Transactions: {debit_count}")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🏦 SBI Statement Transaction Extractor - Final Version")
    print("=" * 60)
    
    # Get password from user
    password = input("🔐 Enter PDF password: ")
    
    if not password:
        print("❌ Password is required. Exiting.")
        return
    
    extractor = FinalSBIExtractor()
    
    # Try statements folder first, then current directory
    statements_dir = os.path.join(current_dir, "statements")
    if os.path.exists(statements_dir):
        pdf_files = glob.glob(os.path.join(statements_dir, "*.pdf"))
        search_dir = statements_dir
        print(f"📁 Using statements folder: {statements_dir}")
    else:
        pdf_files = glob.glob(os.path.join(current_dir, "*.pdf"))
        search_dir = current_dir
        print(f"📁 Using current directory: {current_dir}")
    
    print(f"\n📁 Found {len(pdf_files)} PDF files to process...")
    
    total_transactions = 0
    processed_files = 0
    failed_files = []
    
    for pdf_file in pdf_files:
        transactions = extractor.process_single_pdf(pdf_file, password)
        if transactions > 0:
            processed_files += 1
        else:
            failed_files.append(os.path.basename(pdf_file))
        total_transactions += transactions
    
    print(f"\n🎉 Processing Complete!")
    print(f"✅ Files processed successfully: {processed_files}/{len(pdf_files)}")
    print(f"📊 Total transactions extracted: {total_transactions}")
    
    if failed_files:
        print(f"\n⚠️  Files with no transactions found: {len(failed_files)}")
        for file in failed_files[:5]:  # Show first 5
            print(f"   - {file}")
        if len(failed_files) > 5:
            print(f"   ... and {len(failed_files) - 5} more")
    
    if total_transactions > 0:
        output_file = os.path.join(current_dir, "SBI_Transactions_Final.xlsx")
        extractor.export_to_excel(output_file)
        print(f"\n📁 Excel file created: {output_file}")
        print(f"✨ Ready to use! Open the Excel file to view your transactions.")
    else:
        print("\n❌ No transactions found. Please check:")
        print("   1. Password is correct")
        print("   2. PDF files are in 'statements' folder or current directory")
        print("   3. PDF files are SBI bank statements")
        print("   4. Try different password formats (DOB, Account number, etc.)")
        if search_dir != current_dir:
            print(f"   5. Searched in: {search_dir}")

if __name__ == "__main__":
    main()
