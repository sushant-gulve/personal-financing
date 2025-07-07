# SBI Bank Statement Transaction Extractor

This tool extracts transactions from password-protected SBI bank statement PDFs and exports them to Excel with organized output structure.

## � Folder Structure

```
SBI/
├── statements/                        # 📄 Put your PDF files here
│   ├── 8867301577828022021.pdf
│   ├── 8867301577828022025.pdf
│   └── ... (all your SBI PDFs)
├── extracted_transactions/            # 📊 Generated output
│   ├── excel_files/
│   ├── reports/
│   └── debug_files/
├── sbi_extractor.py                   # 🌟 Main command-line tool
├── run_extractor.bat                  # 🚀 Double-click to run (Windows)
├── run_extractor.ps1                  # 🚀 PowerShell script
└── ... (other scripts)
```

## 🚀 Quick Start (Recommended)

### Step 1: Organize Your Files
1. Create a `statements` folder in the SBI directory
2. Move all your SBI PDF files into the `statements` folder

### Step 2: Run the Extractor

#### Option 1: Double-click (Easiest)
```
Double-click: run_extractor.bat
```

#### Option 2: PowerShell
```powershell
.\run_extractor.ps1
```

#### Option 3: Command Line with Options
```bash
python sbi_extractor.py --input "statements" --output "extracted_transactions"
```

## 📁 Organized Output Structure

The new command-line tool creates a structured output:

```
extracted_transactions/
├── excel_files/
│   ├── SBI_All_Transactions.xlsx     # Main consolidated file
│   ├── SBI_Transactions_2021.xlsx    # Year-wise files
│   ├── SBI_Transactions_2022.xlsx
│   └── SBI_Transactions_2023.xlsx
├── reports/
│   └── summary_report.txt             # Detailed analysis report
└── debug_files/
    └── debug_*.txt                    # Debug files for troubleshooting
```

## 📊 Available Scripts:

1. **sbi_extractor.py** - 🌟 **NEW Command-Line Tool** (recommended)
2. **extract_final.py** - Polished extraction script
3. **extract_improved.py** - Advanced parsing version
4. **extract_consolidated.py** - Enhanced consolidation with multiple sheets
5. **extract_manual.py** - Simple manual password entry
6. **extract_with_password.py** - Secure password input version
7. **diagnose_pdfs.py** - Diagnostic tool to check PDF status

## Common SBI PDF Passwords:
- Your date of birth (DDMMYYYY format)
- Your account number
- Your mobile number
- Your PAN number

## 🔧 Command Line Options

```bash
python sbi_extractor.py [OPTIONS]

Options:
  -i, --input DIR     Input directory containing PDF files (default: statements)
  -o, --output DIR    Output directory (default: extracted_transactions)
  -p, --password PWD  PDF password (will prompt if not provided)
  -h, --help          Show help message
```

### Examples:
```bash
# Extract from statements folder (default)
python sbi_extractor.py

# Extract from custom directory with custom output
python sbi_extractor.py --input "my_pdfs" --output "my_transactions"

# Provide password directly
python sbi_extractor.py --password "your_password"

# If PDFs are in current directory instead of statements folder
python sbi_extractor.py --input "."
```

## 📊 Output Files:

### Excel Files:
- **SBI_All_Transactions.xlsx** - Main consolidated file with multiple sheets:
  - All_Transactions - Complete transaction list
  - Monthly_Summary - Month-wise breakdown
  - File_Summary - Per-file transaction count
- **SBI_Transactions_YYYY.xlsx** - Year-wise separated files

### Reports:
- **summary_report.txt** - Detailed text report with:
  - Financial totals and breakdowns
  - Monthly analysis
  - File processing status
  - Date ranges covered

### Debug Files:
- **debug_*.txt** - Raw text extraction for troubleshooting failed PDFs

## 🚨 Troubleshooting:

### Common Issues:

| Problem | Solution |
|---------|----------|
| **"No PDF files found"** | Ensure PDFs are in `statements` folder; check folder structure |
| **"Input directory does not exist"** | Create `statements` folder and move PDFs there, or use `--input "."` |
| **"Wrong password"** | Try different formats: DOB (DDMMYYYY), Account number, Mobile, PAN |
| **"No transactions found"** | Check `debug_files/` folder for text extraction issues |
| **"Could not extract text"** | PDF might be corrupted, image-based, or heavily encrypted |
| **"Python environment not found"** | Ensure `.venv` directory exists; run from correct directory |

### Debug Process:
1. **Check debug files** - Look in `extracted_transactions/debug_files/`
2. **Review summary report** - Check `extracted_transactions/reports/summary_report.txt`
3. **Verify password** - Try different common password formats
4. **Test single file** - Use `diagnose_pdfs.py` to check individual PDF status

## 📋 Sample Output:

```
🏦 SBI TRANSACTION EXTRACTOR - COMMAND LINE TOOL
============================================================
📁 Output directory created: C:\Users\...\extracted_transactions
📁 Found 39 PDF files to process
============================================================
[1/39] 📄 Processing: 8867301577828022021.pdf
  ✅ Extracted 45 transactions
[2/39] 📄 Processing: 8867301577828022025.pdf
  ✅ Extracted 52 transactions
...
============================================================
🎉 Processing Complete!
✅ Files processed: 35/39
❌ Failed files: 4
📊 Total transactions: 1,247

📊 Generating Excel files...
📋 Generating summary report...

✅ SUCCESS! Extraction completed successfully.
💰 Total Credits: ₹2,45,678.50
💸 Total Debits: ₹1,98,432.25
📈 Net Amount: ₹47,246.25
```

## 🎯 Features:

### Command-Line Tool Features:
- ✅ **Batch processing** - All PDFs processed automatically
- ✅ **Organized output** - Clean folder structure with categorized files
- ✅ **Multiple formats** - Excel files + detailed text reports
- ✅ **Year-wise splitting** - Separate files for each year
- ✅ **Progress tracking** - Real-time processing updates
- ✅ **Error handling** - Debug files for failed extractions
- ✅ **Cross-platform** - Works on Windows, Linux, macOS

### Transaction Extraction Features:
- Handles password-protected PDFs
- Extracts transaction details (date, description, amount, balance)
- Identifies credit/debit transactions automatically
- Exports to Excel with proper formatting
- Provides comprehensive transaction summaries
- Auto-adjusts column widths for readability

## 🔍 Transaction Types Detected:
- NEFT, RTGS, IMPS, UPI payments
- ATM withdrawals and deposits
- POS transactions
- Salary credits
- Interest and dividend payments
- Bank charges and fees
- Cheque transactions
- Cash deposits/withdrawals

## 📈 Analysis Features:
- **Monthly summaries** - Credits, debits, net amount by month
- **Yearly breakdowns** - Annual transaction analysis
- **File-wise reports** - Which PDF contributed what transactions
- **Transaction type analysis** - Credit vs debit breakdowns
- **Date range coverage** - Complete timeline of transactions

## 🎁 Bonus Features:
- **Automatic backups** - Original PDFs remain untouched
- **Duplicate handling** - Maintains all transactions (no artificial removal)
- **Multi-sheet Excel** - Different views of the same data
- **Portable output** - Easy to share and analyze elsewhere

## 📚 Additional Resources:

- **CLI_README.md** - Detailed command-line tool documentation
- **QUICK_START.md** - Quick reference guide for all scripts
- **sample_*.txt** - Sample extracted text files for debugging

## 🎯 Recommendation:

**For best results, use the command-line tool:**
```bash
# Simply double-click this file:
run_extractor.bat

# Or run in PowerShell:
.\run_extractor.ps1
```

This gives you:
- Organized output structure
- Multiple Excel files (main + year-wise)
- Detailed reports
- Better error handling
- Professional presentation

## 📞 Support:

If you encounter issues:
1. Check the `extracted_transactions/debug_files/` folder
2. Review the `summary_report.txt` for detailed information
3. Verify your PDF password using different formats
4. Ensure PDFs are readable SBI statements (not scanned images)

## 🔄 Version History:

- **v1.0** - Basic extraction scripts
- **v2.0** - Password-protected PDF support
- **v3.0** - Multiple parsing methods
- **v4.0** - **NEW** Command-line tool with organized output structure

---

**Ready to extract your transactions? Use the command-line tool for the best experience!** 🚀
