# SBI Transaction Extractor - Command Line Tool

A comprehensive command-line tool to extract transactions from SBI bank statement PDFs with organized output structure.

## 📁 Setup Your Files

### Step 1: Organize Your PDFs
```
SBI/
├── statements/                     # ← Create this folder
│   ├── 8867301577828022021.pdf    # ← Move your PDFs here
│   ├── 8867301577828022025.pdf
│   └── ... (all your SBI PDFs)
└── sbi_extractor.py               # ← The tool
```

### Step 2: Run the Tool

## 🚀 Quick Start

### Option 1: Double-click to run (Windows)
```
Double-click: run_extractor.bat
```

### Option 2: PowerShell
```powershell
.\run_extractor.ps1
```

### Option 3: Command Line
```bash
python sbi_extractor.py
```

## 📁 Organized Output Structure

The tool creates a structured output directory:

```
extracted_transactions/
├── excel_files/
│   ├── SBI_All_Transactions.xlsx     # Main consolidated file
│   ├── SBI_Transactions_2021.xlsx    # Year-wise files
│   ├── SBI_Transactions_2022.xlsx
│   └── SBI_Transactions_2023.xlsx
├── reports/
│   └── summary_report.txt             # Detailed text report
└── debug_files/
    └── debug_*.txt                    # Debug files for failed extractions
```

## 📊 Excel File Contents

### Main File: `SBI_All_Transactions.xlsx`
- **All_Transactions** - Complete transaction list
- **Monthly_Summary** - Month-wise breakdown
- **File_Summary** - Which PDF contributed what

### Year-wise Files
- Separate Excel files for each year
- Easy to analyze specific periods

## 🔧 Command Line Options

```bash
python sbi_extractor.py [OPTIONS]

Options:
  -i, --input DIR     Input directory with PDF files (default: statements)
  -o, --output DIR    Output directory (default: extracted_transactions)
  -p, --password PWD  PDF password (will prompt if not provided)
  -h, --help          Show help message
```

## 📋 Usage Examples

### Extract from statements folder (recommended)
```bash
python sbi_extractor.py
```

### Extract from custom directory
```bash
python sbi_extractor.py --input "my_bank_statements" --output "my_extracted_data"
```

### If PDFs are in current directory
```bash
python sbi_extractor.py --input "."
```

### Provide password directly
```bash
python sbi_extractor.py --password "your_password"
```

## 🎯 What You Get

### 1. Excel Files
- **Complete transaction history** from all PDFs
- **Multiple sheets** with different views
- **Auto-formatted** columns
- **Year-wise separation** for easy analysis

### 2. Summary Report
- **Financial totals** (credits, debits, net)
- **Monthly breakdown** with amounts
- **File processing status**
- **Date range covered**

### 3. Debug Files
- **Text extractions** for failed PDFs
- **Troubleshooting information**
- **Raw data** for manual review

## 🔍 Sample Output

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
📁 Output directory: C:\Users\...\extracted_transactions
📊 Main Excel file: SBI_All_Transactions.xlsx
📋 Summary report: summary_report.txt

💰 Total Credits: ₹2,45,678.50
💸 Total Debits: ₹1,98,432.25
📈 Net Amount: ₹47,246.25
```

## 🔐 Password Tips

Common SBI PDF passwords:
1. **Date of Birth**: DDMMYYYY (e.g., 15031990)
2. **Account Number**: Your full account number
3. **Mobile Number**: Registered mobile number
4. **PAN Number**: Your PAN card number

## 🛠️ Troubleshooting

### Issue: "No PDF files found"
- Ensure PDF files are in the `statements` directory
- Check the `--input` parameter if using custom directory
- Use `--input "."` if PDFs are in current directory

### Issue: "Input directory does not exist" 
- Create a `statements` folder and move your PDFs there
- Or specify the correct directory with `--input`

### Issue: "Wrong password"
- Try different password formats
- Check if PDFs are actually password-protected

### Issue: "No transactions found"
- Check `debug_files/` for text extraction
- Verify PDFs are SBI bank statements

### Issue: "Python environment not found"
- Ensure `.venv` directory exists
- Run from the correct directory

## 🎁 Features

- ✅ **Batch processing** - All PDFs in one go
- ✅ **Organized output** - Clean folder structure
- ✅ **Multiple formats** - Excel files + text reports
- ✅ **Year-wise splitting** - Easy period analysis
- ✅ **Error handling** - Debug files for failures
- ✅ **Progress tracking** - Real-time processing updates
- ✅ **Cross-platform** - Windows batch, PowerShell, Python

## 📞 Support

If you encounter issues:
1. Check the `debug_files/` folder
2. Review the `summary_report.txt`
3. Verify your PDF password
4. Ensure PDFs are readable SBI statements

---

**Ready to extract your transactions? Just run the tool and follow the prompts!** 🎉
